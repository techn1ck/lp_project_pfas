from flask import Blueprint, request, jsonify
from web.db import session

blueprint = Blueprint('api', __name__, url_prefix='/api')


@blueprint.route('/', methods=['POST'])
def api_index():
    pass
    """
    в боте пользователь пишет /start
    отправляется пост запрос на /api с 'username':'@tgusername'
    Возвращаем false или (true и secretkey)
    """

"""
get_user_status(username, secretkey)"
    проверяем в базе данных валидность данных
    возвращаем true или false, либо user, admin, guest etc

"""


@blueprint.route('/operation', methods=['POST'])
def get_objects_list():
    pass
    """
    получаем {username:"user", token:"123", тип объекта, который нужно вернуть}
    проверяем с помощью get_user_status имеет ли пользователь доступ к нужным объектам
    возвращаем список значений
    
    """
