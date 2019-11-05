from datetime import datetime
from flask_login import current_user

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from web.db import Base


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('user.id'))
    id_currency = Column(Integer, ForeignKey('currency.id'))
    currency = relationship('Currency')

    name = Column(String)
    description = Column(String)

    creation_time = Column(String)
    modification_time = Column(String)
    is_actual = Column(Boolean)

    def __init__(self, id_user=0, id_currency=0, name='', description=''):
        if id_user:
            self.id_user = id_user
        elif current_user:
            self.id_user = current_user.get_id()
        self.id_currency = id_currency
        self.name = name
        self.description = description
        self.is_actual = 1
        self.creation_time = datetime.now()
        self.modification_time = None

    def add_form_data(self, data):
        self.name = data.name.data
        self.description = data.description.data
        self.id_currency = data.id_currency.data
        if self.id:
            self.modification_time = datetime.now()

    def invert_is_actual(self):
        if self.is_actual:
            self.is_actual = False
        else:
            self.is_actual = True

    def __repr__(self):
        return f'<Account - {self.name} (ID = {self.id})>'
