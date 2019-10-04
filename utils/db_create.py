import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from web.models import *
from cfg import DB_STRING

if __name__ == '__main__':
    engine = create_engine(DB_STRING)
    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    session.add_all([
        User(id=1, name='test1', telegram='@test1', phone=12345678, email='test@example.com', ),

        Currency(name='Рубль', short_name='RUB', symbol='₽'),
        Currency(name='Доллар', short_name='USD', symbol='$'),
        Currency(name='Евро', short_name='EUR', symbol='€'),
        Currency(name='Чешская крона', short_name='CZK', symbol='Kč'),
    ])


    session.commit()

