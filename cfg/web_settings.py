import os
from datetime import timedelta

SECRET_KEY = os.urandom(32)
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:654654@localhost:5432/test'
REMEMBER_COOKIE_DURATION = timedelta(days=5)
