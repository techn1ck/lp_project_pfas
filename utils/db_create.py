import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

from web.models import Account, Category, Base, Tag, User, Currency, Currency_Rate, create_engine, sessionmaker, current_user
from cfg import DB_STRING


if __name__ == '__main__':
    engine = create_engine(DB_STRING)
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
            "telegram": "technick",
            "name": "Test2",
            "surname": "User2",
            "password": generate_password_hash("111"),
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
 
    """ данные для пользователя 1
    """

    cat1 = Category(id_user=user2.id, parent_id=None, name='ЮФ')
    cat2 = Category(id_user=user2.id, parent_id=None, name='Проекты')
    cat3 = Category(id_user=user2.id, parent_id=None, name='Расходы')
    cat4 = Category(id_user=user2.id, parent_id=None, name='Кредиты')
    cat5 = Category(id_user=user2.id, parent_id=None, name='Взаиморасчеты')

    session.add_all([
        Account(id_user=user2.id, id_currency=currency1.id, name='Наличные, рубли'),
        Account(id_user=user2.id, id_currency=currency2.id, name='Наличные, доллары'),
        Account(id_user=user2.id, id_currency=currency3.id, name='Наличные, евро'),
        Account(id_user=user2.id, id_currency=currency1.id, name='Сбербанк, рубли'),
        Account(id_user=user2.id, id_currency=currency1.id, name='Альфа-банк, расчетный счет, рубли'),
        Account(id_user=user2.id, id_currency=currency2.id, name='Альфа-банк, расчетный счет, доллары'),
        Account(id_user=user2.id, id_currency=currency3.id, name='Альфа-банк, расчетный счет, евро'),
        Account(id_user=user2.id, id_currency=currency1.id, name='Альфа-банк, мой-сейф, рубли'),
        Account(id_user=user2.id, id_currency=currency2.id, name='Альфа-банк, мой-сейф, доллары'),
        Account(id_user=user2.id, id_currency=currency3.id, name='Альфа-банк, мой-сейф, евро'),
        Account(id_user=user2.id, id_currency=currency1.id, name='Альфа-банк, кредит, рубли'),
        Account(id_user=user2.id, id_currency=currency1.id, name='Альфа-банк, кредитная карта, рубли'),
        Account(id_user=user2.id, id_currency=currency1.id, name='__виртуальный счет__, рубли'),
        Account(id_user=user2.id, id_currency=currency4.id, name='Наличные, чешские кроны'),

        cat1,
        cat2,
        cat3,
        cat4,
        cat5,
    ])
    session.commit()


    cat1_1 = Category(id_user=user2.id, parent_id=cat1.id, name='Приход')
    cat1_2 = Category(id_user=user2.id, parent_id=cat1.id, name='ЗП')
    cat1_3 = Category(id_user=user2.id, parent_id=cat1.id, name='Возврат')
    cat1_4 = Category(id_user=user2.id, parent_id=cat1.id, name='Баланс')
    cat1_5 = Category(id_user=user2.id, parent_id=cat1.id, name='Расход')
    cat1_6 = Category(id_user=user2.id, parent_id=cat1.id, name='Расход невозвратный')
    cat1_7 = Category(id_user=user2.id, parent_id=cat1.id, name='_прочее')

    cat2_1 = Category(id_user=user2.id, parent_id=cat2.id, name='Бор')
    cat2_2 = Category(id_user=user2.id, parent_id=cat2.id, name='Ч-3')
    cat2_3 = Category(id_user=user2.id, parent_id=cat2.id, name='Ф-96')
    cat2_4 = Category(id_user=user2.id, parent_id=cat2.id, name='ИнфоСервис')
    cat2_5 = Category(id_user=user2.id, parent_id=cat2.id, name='Пятиречье')

    cat3_1 = Category(id_user=user2.id, parent_id=cat3.id, name='Авто')
    cat3_2 = Category(id_user=user2.id, parent_id=cat3.id, name='Дача')
    cat3_21 = Category(id_user=user2.id, parent_id=cat3.id, name='Дети')
    cat3_3 = Category(id_user=user2.id, parent_id=cat3.id, name='Квартира')
    cat3_4 = Category(id_user=user2.id, parent_id=cat3.id, name='Еда')
    cat3_5 = Category(id_user=user2.id, parent_id=cat3.id, name='Здоровье')
    cat3_6 = Category(id_user=user2.id, parent_id=cat3.id, name='Подарки')
    cat3_7 = Category(id_user=user2.id, parent_id=cat3.id, name='Покупки')
    cat3_8 = Category(id_user=user2.id, parent_id=cat3.id, name='Путешествия')
    cat3_9 = Category(id_user=user2.id, parent_id=cat3.id, name='Развлечения')
    cat3_101 = Category(id_user=user2.id, parent_id=cat3.id, name='Семья', description='в широком смысле')
    cat3_10 = Category(id_user=user2.id, parent_id=cat3.id, name='Спорт')
    cat3_11 = Category(id_user=user2.id, parent_id=cat3.id, name='Транспорт')
    cat3_12 = Category(id_user=user2.id, parent_id=cat3.id, name='Финансы')
    cat3_13 = Category(id_user=user2.id, parent_id=cat3.id, name='Хобби')
    cat3_14 = Category(id_user=user2.id, parent_id=cat3.id, name='_прочее')

    cat4_1 = Category(id_user=user2.id, parent_id=cat4.id, name='Проценты')
    cat4_2 = Category(id_user=user2.id, parent_id=cat4.id, name='Тело')
    cat4_3 = Category(id_user=user2.id, parent_id=cat4.id, name='Досрочное погашение')
    cat4_4 = Category(id_user=user2.id, parent_id=cat4.id, name='_прочее', description='Комиссии, страховки и тд')


    session.add_all([
        cat1_1,
        cat1_2,
        cat1_3,
        cat1_4,
        cat1_5,
        cat1_6,
        cat1_7,

        cat2_1,
        cat2_2,
        cat2_3,
        cat2_4,
        cat2_5,

        cat3_1,
        cat3_2,
        cat3_21,
        cat3_3,
        cat3_4,
        cat3_5,
        cat3_6,
        cat3_7,
        cat3_8,
        cat3_9,
        cat3_10,
        cat3_101,
        cat3_11,
        cat3_12,
        cat3_13,
        cat3_14,

        cat4_1,
        cat4_2,
        cat4_3,
        cat4_4,
    ])
    session.commit()


    cat3_1_1 = Category(id_user=user2.id, parent_id=cat3_1.id, name='Бензин')
    cat3_1_2 = Category(id_user=user2.id, parent_id=cat3_1.id, name='Покупка/продажа')
    cat3_1_3 = Category(id_user=user2.id, parent_id=cat3_1.id, name='Ремонт')
    cat3_1_4 = Category(id_user=user2.id, parent_id=cat3_1.id, name='Улучшайзинг')
    cat3_1_5 = Category(id_user=user2.id, parent_id=cat3_1.id, name='Эксплуатация')

    cat3_2_1 = Category(id_user=user2.id, parent_id=cat3_2.id, name='Коммуналка')
    cat3_2_2 = Category(id_user=user2.id, parent_id=cat3_2.id, name='Покупки')
    cat3_2_3 = Category(id_user=user2.id, parent_id=cat3_2.id, name='Ремонт')

    cat3_21_1 = Category(id_user=user2.id, parent_id=cat3_21.id, name='Детское питание')
    cat3_21_2 = Category(id_user=user2.id, parent_id=cat3_21.id, name='Игрушки')
    cat3_21_3 = Category(id_user=user2.id, parent_id=cat3_21.id, name='Подгузники')
    cat3_21_4 = Category(id_user=user2.id, parent_id=cat3_21.id, name='_прочее')

    cat3_3_1 = Category(id_user=user2.id, parent_id=cat3_3.id, name='Коммуналка')
    cat3_3_2 = Category(id_user=user2.id, parent_id=cat3_3.id, name='Покупки')
    cat3_3_3 = Category(id_user=user2.id, parent_id=cat3_3.id, name='Ремонт')
    cat3_3_4 = Category(id_user=user2.id, parent_id=cat3_3.id, name='Уборка')

    cat3_4_1 = Category(id_user=user2.id, parent_id=cat3_4.id, name='Продукты')
    cat3_4_2 = Category(id_user=user2.id, parent_id=cat3_4.id, name='Доставка')
    cat3_4_3 = Category(id_user=user2.id, parent_id=cat3_4.id, name='Бизнес-ланч')
    cat3_4_4 = Category(id_user=user2.id, parent_id=cat3_4.id, name='Кафе/рестораны')

    cat3_5_1 = Category(id_user=user2.id, parent_id=cat3_5.id, name='Лекарства')
    cat3_5_2 = Category(id_user=user2.id, parent_id=cat3_5.id, name='Врачи')
    cat3_5_3 = Category(id_user=user2.id, parent_id=cat3_5.id, name='Зубы')

    cat3_7_1 = Category(id_user=user2.id, parent_id=cat3_7.id, name='Одежда')
    cat3_7_2 = Category(id_user=user2.id, parent_id=cat3_7.id, name='Обувь')
    cat3_7_3 = Category(id_user=user2.id, parent_id=cat3_7.id, name='Электроника')
    cat3_7_4 = Category(id_user=user2.id, parent_id=cat3_7.id, name='Косметика')
    cat3_7_5 = Category(id_user=user2.id, parent_id=cat3_7.id, name='_прочее')

    cat3_11_1 = Category(id_user=user2.id, parent_id=cat3_11.id, name='Такси')
    cat3_11_2 = Category(id_user=user2.id, parent_id=cat3_11.id, name='Метро')
    cat3_11_3 = Category(id_user=user2.id, parent_id=cat3_11.id, name='Общественный')
    cat3_11_4 = Category(id_user=user2.id, parent_id=cat3_11.id, name='Кар-шеринг')

    cat3_12_1 = Category(id_user=user2.id, parent_id=cat3_12.id, name='Альфа')
    cat3_12_2 = Category(id_user=user2.id, parent_id=cat3_12.id, name='Сбер')
    cat3_12_3 = Category(id_user=user2.id, parent_id=cat3_12.id, name='Налоги')

    cat3_101_1 = Category(id_user=user2.id, parent_id=cat3_101.id, name='Сестра')
    cat3_101_2 = Category(id_user=user2.id, parent_id=cat3_101.id, name='Мама')
    cat3_101_3 = Category(id_user=user2.id, parent_id=cat3_101.id, name='Бабушка')
    cat3_101_4 = Category(id_user=user2.id, parent_id=cat3_101.id, name='Тетя')


    session.add_all([
        cat3_1_1,
        cat3_1_2,
        cat3_1_3,
        cat3_1_4,
        cat3_1_5,

        cat3_2_1,
        cat3_2_2,
        cat3_2_3,

        cat3_21_1,
        cat3_21_2,
        cat3_21_3,
        cat3_21_4,

        cat3_3_1,
        cat3_3_2,
        cat3_3_3,
        cat3_3_4,

        cat3_4_1,
        cat3_4_2,
        cat3_4_3,
        cat3_4_4,

        cat3_5_1,
        cat3_5_2,
        cat3_5_3,

        cat3_7_1,
        cat3_7_2,
        cat3_7_3,
        cat3_7_4,
        cat3_7_5,

        cat3_11_1,
        cat3_11_2,
        cat3_11_3,
        cat3_11_4,

        cat3_12_1,
        cat3_12_2,
        cat3_12_3,

        cat3_101_1,
        cat3_101_2,
        cat3_101_3,
        cat3_101_4,

    ])
    session.commit()

    
    session.close()

