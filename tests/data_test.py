import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import IntegrityError

from web.models import Account, Base, Category, Currency, Operation, Tag, User
from cfg import TestConfig

engine = create_engine(TestConfig.SQLALCHEMY_DATABASE_URI)
session = scoped_session(sessionmaker(bind=engine))

test_user = {
            "telegram": "test_user",
            "name": "Test",
            "surname": "User",
            "password": "test_user",
            "phone": "123",
            "email": "test_user",
            "role": "admin",
            "creation_time": datetime.now(),
            "modification_time": None,
            "is_actual": True
}
test_user['password'] = generate_password_hash("test_user")

operation_form_testdata = {
            "category": 9,
            "account": 2,
            "tags": 1,
            "name": "Test",
            "description": "test operation",
            "value": 111,
}


def add_test_user(user):
    try:
        new_user = User(**user)
        session.add(new_user)
        session.commit()
        session.remove()
    except IntegrityError:
        return 'Такой пользователь уже существует'


if __name__ == "__main__":
    print(add_test_user(test_user))
