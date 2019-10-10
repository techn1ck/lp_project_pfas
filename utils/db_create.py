import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

from web.models import Account, Category, Base, Tag, User, Currency, Currency_Rate, create_engine, sessionmaker, current_user
from cfg import DB_STRING


if __name__ == '__main__':
    engine = create_engine(DB_STRING, echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    
    test_user1 = {
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
    test_user2 = {
            "telegram": "test",
            "name": "Test User 2",
            "surname": "TestTest",
            "password": generate_password_hash("test"),
            "phone": "8111111111",
            "email": "second@user.name",
            "role": "user",
            "creation_time": datetime.now(),
            "modification_time": None,
            "is_actual": True
            }
    
    user1 = User(**test_user1)
    user2 = User(**test_user2)
    currency1 = Currency(name='Рубль', short_name='RUB', symbol='₽')
    currency2 = Currency(name='Доллар', short_name='USD', symbol='$')
    currency3 = Currency(name='Евро', short_name='EUR', symbol='€')    
    currency4 = Currency(name='Чешская крона', short_name='CZK', symbol='Kč')    

    session.add_all([
        user1,
        user2,
        currency1,
        currency2,
        currency3,
        currency4,
    ])
    session.commit()


    """ данные для пользователя 1
    """
    cat1 = Category(id_user=user1.id, parent_id=None, name='Приходы')
    cat2 = Category(id_user=user1.id, parent_id=None, name='Расходы')
    cat3 = Category(id_user=user1.id, parent_id=None, name='Кредиты')
    cat4 = Category(id_user=user1.id, parent_id=None, name='Взаиморасчеты')

    session.add_all([
        Account(id_user=user1.id, id_currency=currency1.id, name='Наличные, рубли'),
        Account(id_user=user1.id, id_currency=currency1.id, name='Сбербанк, рубли'),
        Account(id_user=user1.id, id_currency=currency2.id, name='Наличные, доллары'),
        cat1,
        cat2,
        cat3,
        cat4,
    ])
    session.commit()
   
    session.add_all([
        Category(id_user=user1.id, parent_id=cat1.id, name='ЗП'),
        Category(id_user=user1.id, parent_id=cat1.id, name='Дивиденды'),

        Category(id_user=user1.id, parent_id=cat2.id, name='Еда'),
        Category(id_user=user1.id, parent_id=cat2.id, name='Одежда'),
        Category(id_user=user1.id, parent_id=cat2.id, name='Коммуналка'),
        Category(id_user=user1.id, parent_id=cat2.id, name='Прочее'),

        Tag(id_user=user1.id, name='Тег 1'),
        Tag(id_user=user1.id, name='Тег 2'),
        Tag(id_user=user1.id, name='Тег 3'),
        Tag(id_user=user1.id, name='Тег 4'),
    ])
    session.commit()
 

    
    
    
    session.close()

