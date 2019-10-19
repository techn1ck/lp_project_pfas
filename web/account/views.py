from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import current_user, login_required

from .forms import AccountForm
from web.db import session
from web.account.models import Account
from web.currency.models import Currency

blueprint = Blueprint('account', __name__, url_prefix='/account')


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def accounts_list():
    id = request.values.get('id', default=0, type=int)
    id_user = current_user.get_id()
    account = session.query(Account).filter(Account.id == id and Account.id_user == id_user).one_or_none()

    if not account:
        account = Account()
    elif request.args.get('action', default='', type=str) == 'delete':
        session.delete(account)
        session.commit()
        flash(f"Account was deleted (id='{account.id}', name='{account.name}')")
        return redirect(url_for('account.accounts_list'))

    form = AccountForm(obj=account)
    form.id_currency.choices = [(str(i), n) for i, n in session.query(Currency.id, Currency.name)]

    if form.validate_on_submit():
        account.add_form_data(form)
        session.add(account)
        session.commit()
        if id:
            flash(f"Account was updated (id='{account.id}', name='{account.name}')")
        else:
            flash(f"Account was created (id='{account.id}', name='{account.name}')")
        return redirect(url_for('account.accounts_list'))

    to_form = {
        "title": "Accounts",
        "id": id,
        "form": form,
        "accounts": session.query(Account).filter(Account.id_user == id_user).order_by('id').all(),
    }
    return render_template("account/list.html", **to_form)
