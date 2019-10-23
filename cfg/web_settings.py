import os
from datetime import timedelta


class Config:
    """ Намеренно оставляю нерабочие (для меня) параметры в конфиге
        Чтобы убедиться, что тесты заработали, и мы работаем с правильной базой
    """
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres111:12113@localhost:5432/test'
    REMEMBER_COOKIE_DURATION = timedelta(days=5)


class TestConfig:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://test2:111@localhost:5432/test2'
    WTF_CSRF_ENABLED = False
    TESTING = True
    # BASEDIR = os.path.abspath(os.path.dirname(__file__))  # зачем эта строка? без нее все работает
    SECRET_KEY = 'test'
