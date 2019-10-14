import os
from datetime import timedelta

DB_STRING = 'postgresql+psycopg2://test2:111@localhost:5432/test2'

#CSRF_ENABLED = True # нужен ли этот параметр?
SECRET_KEY = os.urandom(32)
REMEMBER_COOKIE_DURATION = timedelta(days=5)