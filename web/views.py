from werkzeug.security import check_password_hash
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import current_user, login_user
from sqlalchemy.orm import sessionmaker
from web.forms import LoginForm
from web import app
from web.models import User, create_engine
from cfg import DB_STRING

engine = create_engine(DB_STRING)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

@app.route('/')
@app.route('/index')
def index():
    return "Hello World"

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter_by(telegram=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильный логин или пароль')
            return redirect(url_for('login'))
        #login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Вход', form=form)