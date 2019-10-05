from werkzeug.security import check_password_hash
from werkzeug.urls import url_parse
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.orm import sessionmaker
from .forms import LoginForm, AccountForm
from web import app, login
from web.models import Account, Currency, User, create_engine
from cfg import DB_STRING

engine = create_engine(DB_STRING)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html")

@app.route('/accounts/', methods = ['GET', 'POST'])
@login_required
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

@login.user_loader
def load_user(id):
    return session.query(User).get(int(id))
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter_by(telegram=form.telegram.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильный логин/пароль', category='login_error')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Вход', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))