import os
from datetime import timedelta

from .local_settings import TEST_DB_URI, DB_URI


class Config:
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = DB_URI
    REMEMBER_COOKIE_DURATION = timedelta(days=5)


class TestConfig:
    SQLALCHEMY_DATABASE_URI = TEST_DB_URI
    WTF_CSRF_ENABLED = False
    TESTING = True
    SECRET_KEY = 'test'
