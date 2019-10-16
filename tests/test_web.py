import pytest
from web import app, init_db
#from web.models import Account, Base, Category, Currency, User, Operation, Tag


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            init_db(app)
        yield client


def test_login_page(client):
    # проверяем, что в первый раз при заходе на главную страницу нас редиректит на логин и форма доступна
    rv = client.get('/', follow_redirects=True)
    assert b'login_form' in rv.data


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


# def test_login_logout(client):
#     # проверка того, что логин и логаут работает
#     rv = login(client, app.config['USERNAME'], app.config['PASSWORD'])
#     assert b'operations' in rv.data

#     rv = logout(client)
#     assert b'login_form' in rv.data

#     rv = login(client, app.config['USERNAME'] + 'x', app.config['PASSWORD'])
#     assert b'Invalid username' in rv.data

#     rv = login(client, app.config['USERNAME'], app.config['PASSWORD'] + 'x')
#     assert b'Invalid password' in rv.data