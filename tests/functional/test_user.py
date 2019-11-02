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


def test_login_logout(client):
    # проверка того, что логин и логаут работает

    data = login(client, "test_user", "test_user")
    assert 'Главная страница' in data

    data = logout(client)
    assert 'Авторизация' in data

    data = login(client, "test_user" + 'x', "test_user")
    assert 'Неправильный логин/пароль' in data


""" чтобы работало, нужно добавить тестовый счет, категорию и тег
"""
# def test_operation_page(client, init_database):
#     login(client, "test_user", "test_user")
#     # Страница загрузилась, форма доступна (нужно задать форме уникальный css класс,
#     # чтобы точно знать, что это нужная форма)
#     response = client.get('/operation', follow_redirects=True)
#     assert '<h1>Операции</h1>', '<div class="form-group  required">' in response.data.decode('utf-8')

#     # Тест добавления операции
#     operation_form_testdata = {
#         "category": 9,
#         "account": 2,
#         "tags": 1,
#         "name": "Test",
#         "description": "test operation",
#         "value": 111,
#     }
#     query = client.post('/operation/', data=operation_form_testdata, follow_redirects=True)
#     assert 'Операция добавлена' in query.data.decode('utf-8')
