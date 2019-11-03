from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import current_user, login_required

from .forms import AccountForm
from web.db import session
from web.account.models import Account
from web.currency.models import Currency
from web.operation.models import Operation
from web.obj_history.db_history import save_original_state, get_obj_history, get_deleted_objects


blueprint = Blueprint('account', __name__, url_prefix='/account')


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def account_list():
    id_account = request.values.get('id', default=0, type=int)
    id_user = current_user.get_id()
    action = request.args.get('action', default='', type=str)
    account = get_current_account(id_account, id_user)

    if action == 'delete' and account.id:
        if not check_is_empty_account(account.id):
            flash(f"Unable to delete account, it has operations. Please, empty account first", category='error')
            return redirect(url_for('account.account_list'))
        else:
            delete_account(account)
            return redirect(url_for('account.account_list'))

    if action == 'switch' and account.id:
        change_account_actual(account)
        return redirect(url_for('account.account_list'))

    form = AccountForm(obj=account)
    form.id_currency.choices = [(str(i), n) for i, n in session.query(Currency.id, Currency.name)]

    if form.validate_on_submit():
        save_account(account, form, id_account)
        return redirect(url_for('account.account_list'))

    to_form = {
        "title": "Accounts",
        "id": id_account,
        "form": form,
        "current_acc": account,
        "accounts": get_accounts_list(id_user),
        "account_history": get_obj_history('Account', account.id),
        "deleted_accounts": get_deleted_objects('Account'),
    }
    return render_template("account/list.html", **to_form)


def get_current_account(id_account, id_user):
    account = session.query(Account).filter(Account.id == id_account and Account.id_user == id_user).one_or_none()
    if not account:
        account = Account()
    return account


def check_is_empty_account(id_account):
    if not session.query(Operation).filter(Operation.id_account == id_account).first():
        return True


def delete_account(account):
    save_original_state('Account', account.id, 'delete', account)
    session.delete(account)
    session.commit()
    flash(f"Account was deleted (id='{account.id}', name='{account.name}')")


def save_account(account, form, id_account):
    if account.id:
        save_original_state('Account', account.id, 'update', account)
    account.add_form_data(form)
    session.add(account)
    session.commit()
    if id_account:
        flash(f"Account was updated (id='{account.id}', name='{account.name}')")
    else:
        flash(f"Account was created (id='{account.id}', name='{account.name}')")


def change_account_actual(account):
    save_original_state('Account', account.id, 'invert_is_actual', account)
    account.invert_is_actual()
    session.add(account)
    session.commit()
    flash(f"Account was switched (id='{account.id}', name='{account.name}')")


def get_accounts_list(id_user):
    return session.query(Account).filter(Account.id_user == id_user).order_by('id').all()
