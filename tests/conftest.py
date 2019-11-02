import pytest
from cfg.web_settings import TestConfig
from .test_db import engine
from ._initial_data import insert_test_user

from web import create_app
from web.db import Base, session


@pytest.fixture(scope='session')
def client():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    insert_test_user()

    app = create_app(TestConfig)
    with app.test_client() as client:
        yield client
    
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='function')
def login(client):
    client.post('/login', data=dict(
        telegram="test_user",
        password="test_user"
    ), follow_redirects=True)
    yield
    client.get('/logout', follow_redirects=True)
