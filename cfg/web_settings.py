import os
DB_STRING = 'postgresql+psycopg2://postgres:123@localhost:5432/test'

CSRF_ENABLED = True # нужен ли этот параметр?
SECRET_KEY = os.urandom(32)