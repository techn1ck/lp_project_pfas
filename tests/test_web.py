import pytest
from web import app, init_db
#from web.models import Account, Base, Category, Currency, User, Operation, Tag

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123@localhost:5432/test'
app.config['WTF_CSRF_ENABLED'] = False
app.config['USERNAME'] = "mytg"
app.config['PASSWORD'] = "mytg"

operation_form_testdata = {
    "category": 9,
    "account": 2,
    "tags": 1,
    "name": "Test",
    "description": "test operation",
    "value": 111,
}

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
        telegram=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_login_logout(client):
    # проверка того, что логин и логаут работает
    
    rv = login(client, app.config['USERNAME'], app.config['PASSWORD'])
    assert 'Главная страница' in rv.get_data(as_text=True)
    
    rv = logout(client)
    assert 'Авторизация' in rv.get_data(as_text=True)

    rv = login(client, app.config['USERNAME'] + 'x', app.config['PASSWORD'])
    assert 'Неправильный логин/пароль' in rv.get_data(as_text=True)

    rv = login(client, app.config['USERNAME'], app.config['PASSWORD'] + 'x')
    assert 'Неправильный логин/пароль' in rv.get_data(as_text=True)


def test_operation_page(client):
    login(client, app.config['USERNAME'], app.config['PASSWORD'])
    # Страница загрузилась, форма доступна (нужно задать форме уникальный css класс, чтобы точно знать, что это нужная форма)
    rv = client.get('/operations', follow_redirects=True)
    assert '<h1>Операции</h1>', '<div class="form-group  required">' in rv.get_data(as_text=True)

    #Тест добавления операции
    query = client.post('/operations', data=operation_form_testdata, follow_redirects=True)
    assert 'Операция добавлена' in query.get_data(as_text=True)