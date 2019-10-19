import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from web import app
from web.models import Account, Base, Category, Currency, Operation, Tag, User

from cfg import TestConfig
from tests.data_test import test_user, add_test_user


engine = create_engine(TestConfig.SQLALCHEMY_DATABASE_URI)
session = scoped_session(sessionmaker(bind=engine))


@pytest.fixture
def client():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    client = app.test_client()
    app.config.from_object(TestConfig)

    return client


def test_login_page(client):
    # проверяем, что в первый раз при заходе на главную страницу нас редиректит на логин и форма доступна
    response = client.get('/', follow_redirects=True)
    data = response.data.decode('utf-8')
    assert 'login_form' in data


def login(client, username, password):
    add_test_user(test_user)
    response = client.post('/login', data=dict(
        telegram=username,
        password=password
    ), follow_redirects=True)
    return response.data.decode('utf-8')


def logout(client):
    response = client.get('/logout', follow_redirects=True)
    return response.data.decode('utf-8')


def test_login_logout(client):
    # проверка того, что логин и логаут работает

    data = login(client, test_user['telegram'], "test_user")
    assert 'Главная страница' in data

    data = logout(client)
    assert 'Авторизация' in data

    data = login(client, test_user['telegram'] + 'x', test_user['password'])
    assert 'Неправильный логин/пароль' in data


# def test_operation_page(client):
#     login(client, test_user, test_password)
#     # Страница загрузилась, форма доступна (нужно задать форме уникальный css класс, чтобы точно знать, что это нужная форма)
#     rv = client.get('/operations', follow_redirects=True)
#     assert '<h1>Операции</h1>', '<div class="form-group  required">' in rv.get_data(as_text=True)

#     # Тест добавления операции
#     query = client.post('/operations', data=operation_form_testdata, follow_redirects=True)
#     assert 'Операция добавлена' in query.get_data(as_text=True)