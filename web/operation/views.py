from calendar import monthlen
from datetime import date, datetime, timedelta
from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import current_user, login_required
from werkzeug import ImmutableMultiDict

from .forms import OperationForm, OperationsFilterForm
from web.account.models import Account
from web.db import session
from web.obj_history.db_history import save_original_state, get_obj_history, get_deleted_objects
from web.operation.models import Operation
from web.future_operation.models import FutureOperaion  # без импорта не дает сохранить операцию

from .helpers import get_user_accs, get_user_categories, get_user_categories_tree, get_user_tags, get_user_operations, get_tags_objects


blueprint = Blueprint('operation', __name__, url_prefix='/operation')


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def operations():
    id_operation = request.values.get('id', default=0, type=int)
    id_user = current_user.get_id()
    action = request.args.get('action', default='', type=str)
    operation = get_current_operation(id_operation, id_user)

    if action == 'delete' and operation.id:
        delete_operation(operation)
        return redirect(url_for('operation.operations'))

    if action == 'switch' and operation.id:
        change_operation_actual(operation)
        return redirect(url_for('category.categories_list'))

    form = OperationForm(obj=operation)
    form.id_account.choices = get_user_accs(id_user)
    form.tags.choices = get_user_tags(id_user)
    form.id_cat.choices = get_user_categories_tree(id_user)

    if form.submit.data and form.validate_on_submit():
        save_operation(operation, form, id_operation, id_user)
        return redirect(url_for('operation.operations'))

    date_from, date_to = get_date_range()
    filter_form = get_operation_filter_form(id_user, date_from, date_to)

    to_form = {
        "title": "Operations",
        "id": id_operation,
        "form": form,
        "date_from": date_from,
        "date_to": date_to,
        'total_value': 100,
        "filter_form": filter_form,
        "current_operation": operation,
        "operations": get_user_operations(
            id_user,
            date_from,
            date_to,
            request.values.get('filter_id_account', default=0, type=int),
            request.values.get('filter_id_cat', default=0, type=int),
            ),
        "category_history": get_obj_history('Operation', operation.id),
        "deleted_categories": get_deleted_objects('Operation'),
    }
    return render_template("operation/list.html", **to_form)


def get_operation_filter_form(id_user, date_from, date_to):
    filter_form = OperationsFilterForm()
    full_field_process(
        filter_form.date_from,
        date_from.strftime(filter_form.date_from.format)
        )
    full_field_process(
        filter_form.date_to,
        date_to.strftime(filter_form.date_to.format)
        )
    filter_form.filter_id_account.choices = get_user_accs(id_user, not_selected_choise=True)
    filter_form.filter_id_cat.choices = get_user_categories_tree(id_user)
    return filter_form


def full_field_process(field, val):
    field.process(ImmutableMultiDict([(field.short_name, val)]))


def get_date_range():
    str_date_from = request.values.get('date_from', '', type=str)
    str_date_to = request.values.get('date_to', '', type=str)
    today = date.today()

    if str_date_from:
        try:
            date_from = datetime.strptime(str_date_from, "%Y-%m-%d").date()
        except ValueError:
            date_from = date(today.year, today.month, 1)
    else:
        date_from = date(today.year, today.month, 1)

    if str_date_to:
        try:
            date_to = datetime.strptime(str_date_to, "%Y-%m-%d").date()
        except ValueError:
            date_to = date(today.year, today.month, monthlen(today.year, today.month))
    else:
        date_to = date(today.year, today.month, monthlen(today.year, today.month))

    if date_to < date_from:
        date_from = date_to - timedelta(days=monthlen(today.year, today.month))

    return date_from, date_to


def get_current_operation(id_operation, id_user):
    operation = session.query(Operation).filter(Operation.id == id_operation).one_or_none()
    if not operation:
        operation = Operation()
    else:
        operation_account = session.query(Account).filter(Account.id == operation.id_account).one()
        if operation_account.id_user != int(id_user):
            operation = Operation()
    return operation


def delete_operation(operation):
    save_original_state('Operation', operation.id, 'delete', operation)
    session.delete(operation)
    session.commit()
    flash(f"Operation was deleted (id='{operation.id}', name='{operation.name}')")


def change_operation_actual(operation):
    save_original_state('Operation', operation.id, 'invert_is_actual', operation)
    operation.invert_is_actual()
    session.add(operation)
    session.commit()
    flash(f"Operation was switched (id='{operation.id}', name='{operation.name}')")


def save_operation(operation, form, id_operation, id_user):
    if operation.id:
        save_original_state('Operation', operation.id, 'update', operation)
    tags_objects_list = get_tags_objects(form.tags.data, id_user)
    operation.form_processing(form, tags_objects_list, id_operation)
    if not tags_objects_list:
        operation.tags.clear()  # Если просто передавать пустое значение, теги не удаляются полностью
    session.add(operation)
    session.commit()
    if id_operation:
        flash(f"Operation was updated (id='{operation.id}', name='{operation.name}')")
    else:
        flash(f"Operation was created (id='{operation.id}', name='{operation.name}')")
