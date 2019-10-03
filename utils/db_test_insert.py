# Временный файл для добавления тестовых данных
import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

from web.models import Base, User, Currency, Currency_Rate, create_engine, sessionmaker
from cfg import DB_STRING

engine = create_engine(DB_STRING, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

test_user = {
            "telegram": "mytg",
            "name": "Test",
            "surname": "User",
            "password_hash": generate_password_hash("password"),
            "phone": "89000000000",
            "email": "first@user.name",
            "role": "admin",
            "creation_time": datetime.now(),
            "modification_time": datetime.now(),
            "is_actual": True
            }

test_currencies = [
    {"name": "Рубль","short_name": "RUB","symbol": "₽"},
    {"name": "Доллар","short_name": "USD","symbol": "$"},
    {"name": "Евро","short_name": "EUR","symbol": "€"}
]
new_user = User(**test_user)
session.add(new_user)

session.commit()
session.close()