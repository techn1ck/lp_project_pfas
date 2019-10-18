from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship

from web.db import Base


class Currency(Base):
    __tablename__ = 'currency'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    short_name = Column(String)
    symbol = Column(String(2))

    def __init__(self, name, short_name, symbol):
        self.name = name
        self.short_name = short_name
        self.symbol = symbol

    def __repr__(self):
        return f'<Currency: {self.id}, {self.name}>'


class Currency_Rate(Base):
    __tablename__ = 'currency_rate'

    id = Column(Integer, primary_key=True)

    id_account = Column(Integer, ForeignKey('account.id'))
    # id_account_currency = relationship("Account", foreign_keys="Account.id_currency")
    # id_default_currency = relationship("User", foreign_keys="User.id_currency")
    id_account_currency = Column(Integer)
    id_default_currency = Column(Integer)
    rate = Column(Numeric)
    operation_date = Column(Date)

    def __init__(self, id_account_currency, id_default_currency, rate, operation_date):
        self.id_account_currency = id_account_currency
        self.id_default_currency = id_default_currency
        self.rate = rate
        self.operation_date = operation_date

    def __repr__(self):
        return f'<Currency rate: {self.id_account_currency}, {self.id_default_currency}>'