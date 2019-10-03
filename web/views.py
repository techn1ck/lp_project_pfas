from werkzeug.security import check_password_hash
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
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
#@login_required
def index():
    return render_template('base.html')

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
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', title='Вход', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))