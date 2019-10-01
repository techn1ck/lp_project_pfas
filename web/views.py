from flask import render_template, flash, redirect, request
from sqlalchemy.orm import sessionmaker

from web import app
from web.models import Account, create_engine
from .forms import AccountForm
from cfg import DB_STRING

engine = create_engine(DB_STRING)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/accounts/', methods = ['GET', 'POST'])
def accounts():
    form = AccountForm()
    data = session.query(Account).all() 

    if request.method == 'POST' and form.validate_on_submit():
#        if not session.query(Account).filter(Account.id == form.id).count():
        a = Account(form)
        session.add(a)
        session.commit()
        
    return render_template("account_form.html", title = "Accounts", form=form, data=data)