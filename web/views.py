from werkzeug.security import check_password_hash
from werkzeug.urls import url_parse
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.orm import sessionmaker
from .forms import AccountForm, CategoryForm, LoginForm, OperationForm, TagForm
from web import app, login
from web.models import Account, Category, Currency, User, Operation, Tag, create_engine
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


@app.route('/login', methods=['GET', 'POST'])
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


@app.route('/accounts/', methods=['GET', 'POST'])
@login_required
def accounts():
    id = request.values.get('id', default=0, type=int)
    a = session.query(Account).filter(Account.id == id).one_or_none()

    if not a:
        a = Account()
    elif request.args.get('action', default='', type=str) == 'delete':
        session.delete(a)
        session.commit()
        flash(f"Account was deleted (id='{a.id}', name='{a.name}')")
        return redirect(url_for('accounts'))

    form = AccountForm(obj=a)
    form.id_currency.choices = [(str(i), n) for i, n in session.query(Currency.id, Currency.name)]

    if form.validate_on_submit():
        a.add_form_data(form)
        session.add(a)
        session.commit()
        if id:
            flash(f"Account was updated (id='{a.id}', name='{a.name}')")
        else:
            flash(f"Account was created (id='{a.id}', name='{a.name}')")
        return redirect(url_for('accounts'))

    to_form = {
        "title": "Accounts",
        "id": id,
        "form": form,
        "data": session.query(Account).order_by('id').all(),
    }
    return render_template("accounts.html", **to_form)


@app.route('/categories/', methods=['GET', 'POST'])
@login_required
def categories():
    id = request.values.get('id', default=0, type=int)
    c = session.query(Category).filter(Category.id == id).one_or_none()

    if not c:
        c = Category()
    elif request.args.get('action', default='', type=str) == 'delete':
        session.delete(c)
        session.commit()
        flash(f"Category was deleted (id='{c.id}', name='{c.name}')")
        return redirect(url_for('categories'))

    form = CategoryForm(obj=c)
    form.parent_id.choices = get_categories_tree()

    if form.validate_on_submit():
        if form.parent_id.data == "0":
            form.parent_id.data = None
        c.add_form_data(form)
        session.add(c)
        session.commit()
        if id:
            flash(f"Category was updated (id='{c.id}', name='{c.name}')")
        else:
            flash(f"Category was created (id='{c.id}', name='{c.name}')")
        return redirect(url_for('categories'))

    to_form = {
        "title": "Categories",
        "id": id,
        "form": form,
        "data": session.query(Category).order_by('id').all(),
    }
    return render_template("categories.html", **to_form)


def get_categories_tree():
    data = [(str(0), " - НЕТ - "), ('', '')]
    for c in session.query(Category).filter(Category.parent_id == None).order_by('id').all():
        data.append((str(c.id), f"+ {c.name}"))
        if c.children:
            for child in c.children:
                data.append((str(child.id), f"|-- {child.name}"))
            data.append(('', ''))
    return data


@app.route('/operations/', methods=['GET', 'POST'])
@login_required
def operations():
    form = OperationForm()
    user_operations = get_user_operations(current_user.get_id())

    form.account.choices = get_user_accs(current_user.get_id())
    form.category.choices = get_user_categories(current_user.get_id())
    form.tags.choices = get_user_tags(current_user.get_id())
    #  в choises пустой массив, если у пользователя нет счетов\категорий\тегов

    if form.validate_on_submit() and request.method == "POST":
        form_data = {
            "id_cat": int(form.category.data),
            "id_account": int(form.account.data),
            "name": form.name.data,
            "description": form.description.data,
            "value": form.value.data,
            "tags": form.tags.data,
        }
        session.add(Operation(**form_data))
        session.commit()
        flash('Операция добавлена')
        return redirect(url_for('operations'))
    return render_template("operations.html", form=form, operations=user_operations)


def get_user_accs(user_id):
    accounts = []
    result = session.query(Account).filter(Account.id_user == user_id).all()
    # нужно переделать запрос, чтобы  он возвращал не весь счет, а только нужные нам данные, добавить проверку is_actual и сортировку (в порядке чего?)
    if len(result) == 0:  # not len(result) ?
        return accounts  # если у пользователя нет счетов, возвращаем None
    for account in result:
        accounts.append((account.id, account.name))
    return accounts


def get_user_categories(user_id):
    categories = []
    result = session.query(Category).filter(Category.id_user == user_id).all()
    # тоже самое, что и в get_user_accs и сделалать вывод в виде дерева категорий
    if len(result) == 0:
        return categories
    for category in result:
        categories.append((category.id, category.name))
    return categories


def get_user_operations(user_id):
    user_accounts_id = []
    user_accounts = get_user_accs(user_id)
    if len(user_accounts) == 0:
        return
    for account in user_accounts:
        user_accounts_id.append(account[0])
    operations = session.query(Operation).filter(Operation.id_account.in_(user_accounts_id)).order_by(Operation.creation_time.desc()).all()
    return operations


def get_user_tags(user_id):
    user_tags = []
    result = session.query(Tag).filter(Tag.id_user == user_id, Tag.is_actual == True).all()
    if len(result) == 0:  # смотри комментарии get_user_accs
        return user_tags
    for tag in result:
        user_tags.append((tag.id, tag.name))
    return user_tags

@app.route('/reports')
@login_required
def reports():
    return render_template("reports.html")


@app.route('/settings')
@login_required
def settings():
    return render_template("settings.html")


@app.route('/tags/', methods=['GET', 'POST'])
@login_required
def tags():
    id = request.values.get('id', default=0, type=int)
    t = session.query(Tag).filter(Tag.id == id).one_or_none()

    if not t:
        t = Tag()
    elif request.args.get('action', default='', type=str) == 'delete':
        session.delete(t)
        session.commit()
        flash(f"Tag was deleted (id='{t.id}', name='{t.name}')")
        return redirect(url_for('tags'))

    form = TagForm(obj=t)

    if form.validate_on_submit():
        t.add_form_data(form)
        session.add(t)
        session.commit()
        if id:
            flash(f"Tag was updated (id='{t.id}', name='{t.name}')")
        else:
            flash(f"Tag was created (id='{t.id}', name='{t.name}')")
        return redirect(url_for('tags'))

    to_form = {
        "title": "Tags",
        "id": id,
        "form": form,
        "data": session.query(Tag).order_by('id').all(),
    }
    return render_template("tags.html", **to_form)


@app.route('/shared_accounts')
@login_required
def shared_accounts():
    return render_template("shared_accounts.html")
