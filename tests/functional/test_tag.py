import pytest
from web.tag.models import Tag
from web.db import session


tag_data = {
     "id": None,
     "name": "Test tag",
     "description": "Test tag description",
}


@pytest.mark.xfail
def test_tag_no_login(client):
    response = client.get('/tag/', follow_redirects=True)
    assert '<h1>Теги</h1>' in response.data.decode('utf-8')


def test_tag_insert(client, login):
    response = client.get('/tag/', follow_redirects=True)
    assert '<h1>Теги</h1>' in response.data.decode('utf-8')

    query = client.post('/tag/', data=tag_data, follow_redirects=True)
    assert 'was created' in query.data.decode('utf-8')


def test_tag_update(client, login):
    tag = session.query(Tag).filter(Tag.name == tag_data['name']).one_or_none()
    assert tag

    tag_data['id'] = tag.id
    query = client.post('/tag/', data=tag_data, follow_redirects=True)
    assert 'was updated' in query.data.decode('utf-8')


def test_tag_switch_is_actual(client, login):
    tag = session.query(Tag).filter(Tag.name == tag_data['name']).one_or_none()
    assert tag

    query = client.post(f'/tag/?action=switch&id={tag.id}', follow_redirects=True)
    assert 'was switched' in query.data.decode('utf-8')


def test_tag_delete(client, login):
    tag = session.query(Tag).filter(Tag.name == tag_data['name']).one_or_none()
    assert tag

    query = client.post(f'/tag/?action=delete&id={tag.id}', follow_redirects=True)
    assert 'was deleted' in query.data.decode('utf-8')

    tag = session.query(Tag).filter(Tag.name == tag_data['name']).one_or_none()
    assert not tag
