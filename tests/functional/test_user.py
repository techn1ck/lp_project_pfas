def test_home_page(client):

    response = client.get('/', follow_redirects=True)
    data = response.data.decode('utf-8')

    assert response.status_code == 200
    assert 'login_form' in data


def login(client, username, password):
    response = client.post('/login', data=dict(
        telegram=username,
        password=password
    ), follow_redirects=True)
    return response.data.decode('utf-8')


def logout(client):
    response = client.get('/logout', follow_redirects=True)
    return response.data.decode('utf-8')


def test_login_logout(client, init_database):
    # проверка того, что логин и логаут работает

    data = login(client, "test_user", "test_user")
    assert 'Главная страница' in data

    data = logout(client)
    assert 'Авторизация' in data

    data = login(client, "test_user" + 'x', "test_user")
    assert 'Неправильный логин/пароль' in data


# def test_operation_page(client):
#     login(client, test_user, test_password)
#     # Страница загрузилась, форма доступна (нужно задать форме уникальный css класс,
#     # чтобы точно знать, что это нужная форма)
#     rv = client.get('/operations', follow_redirects=True)
#     assert '<h1>Операции</h1>', '<div class="form-group  required">' in rv.get_data(as_text=True)

#     # Тест добавления операции
#     query = client.post('/operations', data=operation_form_testdata, follow_redirects=True)
#     assert 'Операция добавлена' in query.get_data(as_text=True)
# operation_form_testdata = {
#     "category": 9,
#     "account": 2,
#     "tags": 1,
#     "name": "Test",
#     "description": "test operation",
#     "value": 111,
# }
