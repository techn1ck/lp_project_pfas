from werkzeug.security import check_password_hash
from werkzeug.urls import url_parse
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.orm import sessionmaker
from .forms import AccountForm, CategoryForm, LoginForm, TagForm
from .tree import Tree
from web import app, login
from web.models import Account, Category, Currency, Tag, User, create_engine
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


@app.route('/accounts/', methods = ['GET', 'POST'])
@login_required
def accounts():
    id = request.values.get('id', default=0, type=int)
    id_user = current_user.get_id()
    account = session.query(Account).filter(Account.id == id and Account.id_user == id_user).one_or_none()

    if not account:
        account = Account()
    elif request.args.get('action', default='', type=str) == 'delete':
        session.delete(account)
        session.commit()
        flash(f"Account was deleted (id='{account.id}', name='{account.name}')")
        return redirect(url_for('accounts'))

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
        return redirect(url_for('accounts'))

    to_form = {
        "title" : "Accounts",
        "id" : id,
        "form" : form,
        "data" : session.query(Account).filter(Account.id_user == id_user).order_by('id').all(),
    }
    return render_template("accounts.html", **to_form)


@app.route('/categories/', methods = ['GET', 'POST'])
@login_required
def categories():
    id = request.values.get('id', default=0, type=int)
    id_user = current_user.get_id()
    category = session.query(Category).filter(Category.id == id and Category.id_user == id_user).one_or_none()

    if not category:
        category = Category()
    elif request.args.get('action', default='', type=str) == 'delete':
        session.delete(category)
        session.commit()
        flash(f"Category was deleted (id='{category.id}', name='{category.name}')")
        return redirect(url_for('categories'))

    form = CategoryForm(obj=category)
    data = session.query(Category).filter(Category.id_user == id_user).order_by('id').all()
    tree = Tree(data)
    form.parent_id.choices = tree.return_choises()

    if form.validate_on_submit():
        if form.parent_id.data == "0":
            form.parent_id.data = None
        category.add_form_data(form)
        session.add(category)
        session.commit()
        if id:
            flash(f"Category was updated (id='{category.id}', name='{category.name}')")
        else:
            flash(f"Category was created (id='{category.id}', name='{category.name}')")
        return redirect(url_for('categories'))

    to_form = {
        "title" : "Categories",
        "id" : id,
        "form" : form,
        "data" : data,
    }
    return render_template("categories.html", **to_form)


@app.route('/operations')
@login_required
def operations():
    return render_template("operations.html")


@app.route('/reports')
@login_required
def reports():
    return render_template("reports.html")


@app.route('/settings')
@login_required
def settings():
    return render_template("settings.html")


@app.route('/tags/', methods = ['GET', 'POST'])
@login_required
def tags():
    id = request.values.get('id', default=0, type=int)
    id_user = current_user.get_id()
    tag = session.query(Tag).filter(Tag.id == id and Tag.id_user == id_user).one_or_none()

    if not tag:
        tag = Tag()
    elif request.args.get('action', default='', type=str) == 'delete':
        session.delete(tag)
        session.commit()
        flash(f"Tag was deleted (id='{tag.id}', name='{tag.name}')")
        return redirect(url_for('tags'))

    form = TagForm(obj=tag)

    if form.validate_on_submit():
        tag.add_form_data(form)
        session.add(tag)
        session.commit()
        if id:
            flash(f"Tag was updated (id='{tag.id}', name='{tag.name}')")
        else:
            flash(f"Tag was created (id='{tag.id}', name='{tag.name}')")
        return redirect(url_for('tags'))

    to_form = {
        "title" : "Tags",
        "id" : id,
        "form" : form,
        "data" : session.query(Tag).filter(Tag.id_user == id_user).order_by('id').all(),
    }
    return render_template("tags.html", **to_form)


@app.route('/shared_accounts')
@login_required
def shared_accounts():
    return render_template("shared_accounts.html")
