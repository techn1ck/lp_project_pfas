from sqlalchemy import create_engine, Table, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


shared_acc_user_table = Table('shared_acc_user', Base.metadata,
    Column('id_user', Integer, ForeignKey('user.id_user')),
    Column('id_shared_acc', Integer, ForeignKey('shared_account.id_shared_acc')),
    Column('user_ratio', Float)
)


class User(Base):
    __tablename__ = 'user'

    id_user = Column(Integer, primary_key=True)

    telegram = Column(String, unique=True)
    name = Column(String)
    surname = Column(String)
    phone = Column(Integer, unique=True)
    email = Column(String, unique=True)
    role = Column(String) # 'user', 'admin', 'guest', etc

    # Вопрос: можно ли таким образом ссылаться на запись (id_user) внутри самой таблицы?
    creator_id_user = Column(Integer, ForeignKey('user.id_user'))
    creatures = relationship('User') # а так же получать список всех 
    
    # Вопрос: как сейчас принято хранить даты?
    # А то я по старой памяти пытаюсь хранить в TimeStamp
    creation_date = Column(Integer) 

    was_modified = Column(Boolean)
    is_actual = Column(Boolean)

    # связка со связанными аккаунтами (многие ко многим) через промежуточную таблицу
    # Вопрос: лучше делать через back_populates или backref?
    shared_accounts = relationship(
        "Shared_Account",
        secondary=shared_acc_user_table,
        back_populates="users")
    
    accounts = relationship('Accounts')


    def __init__ (self, id_user, name='', surname='', telegram='', ):
        pass


    def __repr__ (self):
        return f'<User: {self.id_user}, {self.telegram}>'



class Account(Base):
    __tablename__ = 'Account'

    id_account = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('user.id_user'))
    id_currency = Column(Integer, ForeignKey('currency.id_currency'))
    currency = relationship('Currency')

    name = Column(String)
    decscription = Column(String)


    def __init__ (self, id_user, name='', surname='', telegram='', ):
        pass


    def __repr__ (self):
        return f'<Account: {self.id_account}, {self.name}>'




class Shared_Account(Base):
    __tablename__ = 'Shared_Account'

    id_shared_acc = Column(Integer, primary_key=True)
    owner_id_user = Column(Integer, ForeignKey('user.id_user'))
    id_currency = Column(Integer, ForeignKey('currency.id_currency'))
    currency = relationship('Currency')

    name = Column(String)
    decscription = Column(String)

    users = relationship(
        "User",
        secondary=shared_acc_user_table,
        back_populates="shared_accounts")


    def __init__ (self, id_user, name='', surname='', telegram='', ):
        pass


    def __repr__ (self):
        return f'<Shared_Account: {self.id_account}, {self.name}>'



class Currency(Base):
    __tablename__ = 'Currency'

    id_currency = Column(Integer, primary_key=True)
    short_name = Column(String)
    name = Column(String)


    def __init__ (self, id_user, name='', surname='', telegram='', ):
        pass


    def __repr__ (self):
        return f'<Currency: {self.id_currency}, {self.name}>'



engine = create_engine('postgresql+psycopg2://test2:111@localhost:5432/test2')
Base.metadata.create_all(engine)