import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from datetime import datetime, date

from web.models import Base, User, Currency, Currency_Rate, create_engine, sessionmaker
from cfg import DB_STRING
#engine = create_engine(DB_STRING, echo=True)


test_user = {
            "telegram": "@mytg",
            "name": "Test",
            "surname": "User",
            "phone": "+79000000000",
            "email": "first@user.name",
            "role": "admin",
            "creator_id_user": "1",
            "creation_time": datetime.now(),
            "modification_time": datetime.now(),
            "is_actual": True,
            "id_default_currency": 1
            }

test_currencies = [
    {"name": "Рубль","short_name": "RUB","symbol": "₽"},
    {"name": "Доллар","short_name": "USD","symbol": "$"},
    {"name": "Евро","short_name": "EUR","symbol": "€"}
]