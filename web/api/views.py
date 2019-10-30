import json
from decimal import Decimal
from flask import Blueprint, request, jsonify
from web.db import session
from werkzeug.routing import BaseConverter

from web.user.models import User
from web.operation.models import Operation
from web.category.models import Category
from web.tag.models import Tag

from web.operation.helpers import get_user_operations, get_user_accs, get_operation_tags_names, get_user_categories, get_user_tags

blueprint = Blueprint('api', __name__, url_prefix='/api')


@blueprint.route('/', methods=['GET', 'POST'])
def api_index():
    if request.method == "GET":
        return "API"
    """
    в боте пользователь пишет /start
    отправляется пост запрос на /api с 'username':'@tgusername'
    Возвращаем false или (true и secretkey)
    """


"""
get_user_status(username, secretkey):"
    вспомогательная функция
    проверяем в базе данных валидность данных
    возвращаем id пользователя

"""

@blueprint.route('/<secretkey>/get/<obj>/', methods=['GET', 'POST'])
def get_objects_list(secretkey, obj):
    '''
    возможно в параметрах нужно еще передавать кол-во объектов, сейчас я по-умолчанию поставил 5 последних

    здесь проверка валидности секретного ключа и получение id нужного пользователя
    с помощью функции get_user_status
    '''
    user_id = 2
    obj_count = 5
    responce = []
    if obj == "operations":
        operations = get_user_operations(user_id)
        for operation in operations[0:obj_count]:
            # подумать какие поля от операции нужно передавать в телеграм
            dict_operation = dict(operation.__dict__)
            del(dict_operation['_sa_instance_state'])
            dict_operation['tags'] = get_operation_tags_names(int(operation.id))
            responce.append(dict_operation)
    elif obj == "categories":
        responce = get_user_categories(user_id)
    elif obj == "tags":
        responce = get_user_tags(user_id)
    elif obj == "accounts":
        responce == get_user_accs(user_id)
    else:
        pass
    return json.dumps(responce, default=str, ensure_ascii=False)
