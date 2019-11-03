from werkzeug.security import generate_password_hash
from datetime import datetime

from web.currency.models import Currency
from web.user.models import User
from .test_db import session


def insert_test_user():
    user = {
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
    new_user = User(**user)
    session.add(new_user)
    session.commit()


def insert_currency():
    currency = Currency(name='Рубль', short_name='RUB', symbol='₽')
    session.add(currency)
    session.commit()


def get_currency_id():
    currency = session.query(Currency).filter(Currency.name == 'Рубль').one_or_none()
    return currency.id
