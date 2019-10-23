import pytest
from werkzeug.security import generate_password_hash
from datetime import datetime
from cfg.web_settings import TestConfig
from .test_db import engine, session

from web import create_app
from web.user.models import User
from web.db import Base


@pytest.fixture(scope='module')
def client():
    flask_app = create_app(TestConfig)
    testing_client = flask_app.test_client()

    # Контекст приложения
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client

    ctx.pop()


@pytest.fixture(scope='module')
def init_database():
    """ При очистке БД в конце функции тесты вылетают с ошибкой
    """
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    test_user = {
        "telegram": "test_user",
        "name": "Test",
        "surname": "User",
        "password": generate_password_hash("test_user"),
        "phone": "123",
        "email": "test_user",
        "role": "admin",
        "creation_time": datetime.now(),
        "modification_time": None,
        "is_actual": True
    }

    new_user = User(**test_user)
    session.add(new_user)
    session.commit()

    yield new_user

    # Base.metadata.drop_all(engine)  # почему-то выдает ошибку, перенес в начало
    session.close()
