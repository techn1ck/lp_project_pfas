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

    creator_id_user = Column(Integer, ForeignKey('user.id_user'))
    creatures = relationship('User')
    
    creation_time = Column(String) 
    modification_time = Column(String)
    is_actual = Column(Boolean)

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
    __tablename__ = 'account'

    id_account = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('user.id_user'))
#    id_currency = Column(Integer, ForeignKey('currency.id_currency'))
#    currency = relationship('Currency')

    name = Column(String)
    decscription = Column(String)

    def __init__ (self, id_user, name='', surname='', telegram='', ):
        pass

    def __repr__ (self):
        return f'<Account: {self.id_account}, {self.name}>'


class Shared_Account(Base):
    __tablename__ = 'shared_account'

    id_shared_acc = Column(Integer, primary_key=True)
    owner_id_user = Column(Integer, ForeignKey('user.id_user'))
#    id_currency = Column(Integer, ForeignKey('currency.id_currency'))
#    currency = relationship('Currency')

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

