import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

from web.models import Base, User, Currency, Currency_Rate, create_engine, sessionmaker
from cfg import DB_STRING

if __name__ == '__main__':
    engine = create_engine(DB_STRING)
    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    test_user = {
            "telegram": "mytg",
            "name": "Test",
            "surname": "User",
            "password": generate_password_hash("mytg"),
            "phone": "89000000000",
            "email": "first@user.name",
            "role": "admin",
            "creation_time": datetime.now(),
            "modification_time": None,
            "is_actual": True
            }
    session.add_all([
        User(**test_user),
        Currency(name='Рубль', short_name='RUB', symbol='₽'),
        Currency(name='Доллар', short_name='USD', symbol='$'),
        Currency(name='Евро', short_name='EUR', symbol='€'),
        Currency(name='Чешская крона', short_name='CZK', symbol='Kč'),
    ])


    session.commit()
    session.close()

