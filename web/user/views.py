from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from .forms import LoginForm
from web.db import session
from web.user.models import User

blueprint = Blueprint('user', __name__)


@blueprint.route('/')
@blueprint.route('/index')
@login_required
def index():
    return render_template("index.html")


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter_by(telegram=form.telegram.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильный логин/пароль', category='login_error')
            return redirect(url_for('user.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user.index')
        return redirect(next_page)
    return render_template('user/login.html', title='Вход', form=form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user.index'))


@blueprint.route('/settings')
@login_required
def user_settings():
    return render_template("user/settings.html")
