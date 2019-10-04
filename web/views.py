from flask import render_template, flash, redirect, request
from sqlalchemy.orm import sessionmaker

from web import app
from web.models import Account, Currency, User, create_engine
from .forms import AccountForm
from cfg import DB_STRING


engine = create_engine(DB_STRING)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


@app.route('/')
@app.route('/index')
def index():
    for user in session.query(User).all():
        flash(f"Current user {user}")

    return render_template("index.html")


@app.route('/accounts/', methods = ['GET', 'POST'])
def accounts():
    id = request.args.get('id', default = 0, type = int)
    action = request.args.get('action', default = '', type = str)

    flash(id)

    print(request.args)

    a = None
    if id:
        a = session.query(Account).filter(Account.id == id).one_or_none()

    if not a:
        a = Account()
    elif action == 'delete':
        session.delete(a)
        session.commit()
        a = Account()

    form = AccountForm(obj=a)
    form.id_currency.choices = [(str(id_), name) for id_, name in session.query(Currency.id, Currency.name)]

    if form.validate_on_submit():
        a.add_form_data(form)
        session.add(a)
        session.commit()
        flash(f"Successfully created a new Account (id='{a.id}', name='{a.name}')")

    to_form = {
        "title" : "Accounts",
        "action" : action,
        "form" : form,
        "data" : session.query(Account).all(),
    }

    return render_template("account_form.html", **to_form)