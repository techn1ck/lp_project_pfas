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
    user_id = current_user.get_id()
    user_operations = get_user_operations(user_id)  # для вывода текущих операций
    operation_id = request.values.get('id', default=0, type=int)

    if operation_id:
        current_operation = session.query(Operation).filter(Operation.id == operation_id).one_or_none()
    else:
        current_operation = Operation()

    form.account.choices = get_user_accs(user_id)
    form.category.choices = get_user_categories(user_id)
    form.tags.choices = get_user_tags(user_id)
    #  в choises должен быть пустой массив, если у пользователя нет счетов\категорий\тегов, иначе выдает exception

    if request.method == "GET" and request.args.get('action', default='', type=str) == 'delete':  # удаление
        session.delete(current_operation)
        session.commit()
        # нужно добавить проверку, чтобы юзер не мог удалять чужие операции введя id в get запросе вручную
        flash(f'Операция удалена. id {current_operation.id}')
        return redirect(url_for('operations'))

    elif request.method == "GET" and request.args.get('action', type=str) == "update":
        form.account.default = current_operation.id_account
        form.category.default = current_operation.id_cat
        form.tags.default = get_operation_tags_id(operation_id)
        form.name.default = current_operation.name
        form.description.default = current_operation.description
        form.value.default = current_operation.value
        form.process()  # отрендерить форму заного

    elif form.validate_on_submit() and request.method == "POST":  # Отправка формы
        tags_objects_list = get_tags_objects(form.tags.data, user_id)

        current_operation.form_processing(form, tags_objects_list, operation_id)
        if not tags_objects_list:
            current_operation.tags.clear()  # Если просто передавать пустое значение, теги не удаляются полностью

        session.add(current_operation)
        session.commit()

        if operation_id:
            flash(f'Операция обновлена')
        else:
            flash(f'Операция добавлена')

        return redirect(url_for('operations'))

    return render_template("operations.html", form=form, operations=user_operations)


"""
Методы ниже оставить здесь, в модели добавить или просто в отдельный файл?
"""


def get_user_accs(id_user):
    result = session.query(Account.id, Account.name).filter(Account.id_user == id_user).all()
    if result:
        return [(account.id, account.name) for account in result]
    return []  # wtfforms чтобы отрисовать форму требует список, даже если он пустой


def get_user_categories(id_user):  # добавить вывод в виде дерева
    result = session.query(Category.id, Category.name).filter(Category.id_user == id_user).all()
    if result:
        return [(category.id, category.name) for category in result]
    return []


def get_user_tags(id_user):
    result = session.query(Tag.id, Tag.name).filter(Tag.id_user == id_user, Tag.is_actual == True).all()
    if result:
        return [(user_tags.id, user_tags.name) for user_tags in result]
    return []


def get_operation_tags_id(operation_id):
    tags_id = []
    result = session.query(Operation).filter(Operation.id == operation_id).one_or_none()
    if result:
        for tag in result.tags:
            tags_id.append(tag.id)
    return tags_id


def get_user_operations(id_user):
    user_accounts = get_user_accs(id_user)
    if not user_accounts:
        return
    user_accounts_id = []  # как это написать в одну строку?
    user_accounts_id = [account[0] for account in user_accounts]
    # В данный момент, вместо названий операций и категорий выводятся id, возможно ли с помощью sql запроса сразу выдирать названия или лучше использовать другой способ?
    operations = session.query(Operation).filter(Operation.id_account.in_(user_accounts_id)).order_by(Operation.creation_time.desc()).all()
    if operations:
        return operations


def get_tags_objects(tags_id_list, id_user):  # wtfforms MultipleSelectField в data возвращает список выбранных id
    tag_objects_list = []
    if tags_id_list:
        for tag_id in tags_id_list:
            query = session.query(Tag).filter(Tag.id == tag_id, Tag.id_user == id_user).one_or_none()
            if query:
                tag_objects_list.append(query)
            else:
                pass  # Если такого тега нет, добавить новый объект и вернуть его? Откуда брать id тогда? Надо тогда еще имена передавать
        return tag_objects_list
    else:
        return


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
