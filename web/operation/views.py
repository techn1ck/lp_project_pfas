from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import current_user, login_required

from .forms import OperationForm
from web.db import session
from web.tree import Tree
from web.account.models import Account
from web.category.models import Category
from web.operation.models import Operation
from web.future_operation.models import FutureOperaion  # без импорта не дает сохранить операцию

from web.tag.models import Tag


blueprint = Blueprint('operation', __name__, url_prefix='/operation')


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def operations():
    form = OperationForm()
    user_id = current_user.get_id()
    user_operations = get_user_operations(user_id)  # для вывода текущих операций
    operation_id = request.values.get('id', default=0, type=int)

    if operation_id:
        current_operation = session.query(Operation).filter(Operation.id == operation_id).one_or_none()
    else:
        current_operation = Operation()

    form.account.choices = get_user_accs(user_id)
    form.tags.choices = get_user_tags(user_id)

    categories = session.query(Category).filter(Category.id_user == user_id).order_by('id').all()
    tree = Tree(categories)
    form.category.choices = tree.return_choises()

    #  в choises должен быть пустой массив, если у пользователя нет счетов\категорий\тегов, иначе выдает exception

    if request.method == "GET" and request.args.get('action', default='', type=str) == 'delete':  # удаление
        session.delete(current_operation)
        session.commit()
        # нужно добавить проверку, чтобы юзер не мог удалять чужие операции введя id в get запросе вручную
        flash(f'Операция удалена. id {current_operation.id}')
        return redirect(url_for('operation.operations'))

    elif request.method == "GET" and request.args.get('action', type=str) == "update":
        form.account.default = current_operation.id_account
        form.category.default = current_operation.id_cat
        form.tags.default = get_operation_tags_id(operation_id)
        form.name.default = current_operation.name
        form.description.default = current_operation.description
        form.value.default = current_operation.value
        form.process()  # отрендерить форму заного

    elif form.validate_on_submit() and request.method == "POST":  # Отправка формы
        tags_objects_list = get_tags_objects(form.tags.data, user_id)

        current_operation.form_processing(form, tags_objects_list, operation_id)
        if not tags_objects_list:
            current_operation.tags.clear()  # Если просто передавать пустое значение, теги не удаляются полностью

        session.add(current_operation)
        session.commit()

        if operation_id:
            flash(f'Операция обновлена')
        else:
            flash(f'Операция добавлена')

        return redirect(url_for('operation.operations'))

    return render_template("operation/list.html", form=form, operations=user_operations)


"""
Методы ниже оставить здесь, в модели добавить или просто в отдельный файл?
"""


def get_user_accs(id_user):
    result = session.query(Account.id, Account.name).filter(Account.id_user == id_user).all()
    if result:
        return [(account.id, account.name) for account in result]
    return []  # wtfforms чтобы отрисовать форму требует список, даже если он пустой


def get_user_categories(id_user):  # добавить вывод в виде дерева
    result = session.query(Category.id, Category.name).filter(Category.id_user == id_user).all()
    if result:
        return [(category.id, category.name) for category in result]
    return []


def get_user_tags(id_user):
    result = session.query(Tag.id, Tag.name).filter(Tag.id_user == id_user, Tag.is_actual == True).all()
    if result:
        return [(user_tags.id, user_tags.name) for user_tags in result]
    return []


def get_operation_tags_id(operation_id):
    tags_id = []
    result = session.query(Operation).filter(Operation.id == operation_id).one_or_none()
    if result:
        for tag in result.tags:
            tags_id.append(tag.id)
    return tags_id


def get_user_operations(id_user):
    user_accounts = get_user_accs(id_user)
    if not user_accounts:
        return
    user_accounts_id = []  # как это написать в одну строку?
    user_accounts_id = [account[0] for account in user_accounts]
    # В данный момент, вместо названий операций и категорий выводятся id,
    # возможно ли с помощью sql запроса сразу выдирать названия или лучше использовать другой способ?
    operations = session.query(Operation).\
        filter(Operation.id_account.in_(user_accounts_id)).\
        order_by(Operation.creation_time.desc()).all()
    if operations:
        return operations


def get_tags_objects(tags_id_list, id_user):  # wtfforms MultipleSelectField в data возвращает список выбранных id
    tag_objects_list = []
    if tags_id_list:
        for tag_id in tags_id_list:
            query = session.query(Tag).filter(Tag.id == tag_id, Tag.id_user == id_user).one_or_none()
            if query:
                tag_objects_list.append(query)
            else:
                pass
                # Если такого тега нет, добавить новый объект и вернуть его?
                # Откуда брать id тогда? Надо тогда еще имена передавать
        return tag_objects_list
    else:
        return
