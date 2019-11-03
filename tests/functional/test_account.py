import pytest
from web.account.models import Account
# from web.currency.models import Currency
from web.db import session


def get_currency_id():
    # currency = session.query(Currency).filter(Currency.name == 'Рубль').one_or_none()
    # print(currency.id)
    # return currency.id
    return 1


page_title = '<h1>Счета</h1>'
page_url = '/account/'
obj = Account
data_ = {
     "id": None,
     "name": "Test " + page_url,
     "description": "Test acc description",
     "id_currency": get_currency_id(),
}


def get_obj(obj):
    return session.query(obj).filter(obj.name == data_['name']).one_or_none()


@pytest.mark.xfail
def test_no_login(client):
    response = client.get(page_url, follow_redirects=True)
    assert page_title in response.data.decode('utf-8')


def test_insert(client, login):
    response = client.get(page_url, follow_redirects=True)
    assert page_title in response.data.decode('utf-8')

    query = client.post(page_url, data=data_, follow_redirects=True)
    assert 'was created' in query.data.decode('utf-8')


def test_update(client, login):
    testing_object = get_obj(obj)
    assert testing_object

    data_['id'] = testing_object.id
    query = client.post(page_url, data=data_, follow_redirects=True)
    assert 'was updated' in query.data.decode('utf-8')


def test_switch_is_actual(client, login):
    testing_object = get_obj(obj)
    assert testing_object

    query = client.post(f'{page_url}?action=switch&id={testing_object.id}', follow_redirects=True)
    assert 'was switched' in query.data.decode('utf-8')


def test_delete(client, login):
    testing_object = get_obj(obj)
    assert testing_object

    query = client.post(f'{page_url}?action=delete&id={testing_object.id}', follow_redirects=True)
    assert 'was deleted' in query.data.decode('utf-8')

    testing_object = get_obj(obj)
    assert not testing_object
