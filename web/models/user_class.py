from ._service import *
from .shared_classes import shared_acc_user_table


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)

    telegram = Column(String, unique=True)
    name = Column(String)
    surname = Column(String)
    phone = Column(Integer, unique=True)
    email = Column(String, unique=True)
    role = Column(String) # 'user', 'admin', 'guest', etc

    creator_id_user = Column(Integer, ForeignKey('user.id'))
    creatures = relationship('User')
    
    creation_time = Column(DateTime)
    modification_time = Column(DateTime)
    is_actual = Column(Boolean)

    shared_accounts = relationship(
        "SharedAccount",
        secondary=shared_acc_user_table,
        back_populates="users")
    
    accounts = relationship('Account')
    categories = relationship('Category')

    id_default_currency = Column(Integer, ForeignKey('currency.id'))
    currency = relationship('Currency')

    def __init__ (self, telegram, name, surname, phone, email, role, creator_id_user, creation_time, modification_time, is_actual, id_default_currency):
        self.telegram = telegram
        self.name = name
        self.surname = surname
        self.phone = phone
        self.email = email
        self.role = role
        self.creator_id_user = creator_id_user
        self.creation_time = creation_time
        self.modification_time = modification_time
        self.is_actual = is_actual
        self.id_default_currency = id_default_currency


    def __repr__ (self):
        return f'<User: {self.id}, {self.telegram}>'
