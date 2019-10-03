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
    form = AccountForm()
    form.currency.choices = [(str(id_), name) for id_, name in session.query(Currency.id, Currency.name)]

    data = session.query(Account).all() 

    if form.validate_on_submit():
        a = Account()
        a.add_from_form(form)
        session.add(a)
        session.commit()
        flash(f"Successfully created a new Account (id='{a.id}', name='{a.name}')")
        
    return render_template("account_form.html", title = "Accounts", form=form, data=data)