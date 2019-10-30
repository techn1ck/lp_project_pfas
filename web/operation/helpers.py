from web.db import session
from web.account.models import Account
from web.category.models import Category
from web.operation.models import Operation
from web.tag.models import Tag


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
    # В данный момент, вместо названий операций и категорий выводятся id,
    # возможно ли с помощью sql запроса сразу выдирать названия или лучше использовать другой способ?
    operations = session.query(Operation).\
        filter(Operation.id_account.in_(user_accounts_id)).\
        order_by(Operation.creation_time.desc()).all()
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
                pass
                # Если такого тега нет, добавить новый объект и вернуть его?
                # Откуда брать id тогда? Надо тогда еще имена передавать
        return tag_objects_list
    else:
        return


def get_operation_tags_names(operation_id):
    tags_names = []
    result = session.query(Operation).filter(Operation.id == operation_id).one_or_none()
    if result:
        for tag in result.tags:
            tags_names.append(tag.name)
    return tags_names