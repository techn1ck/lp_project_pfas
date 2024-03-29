from ._service import *
from .operation import operation_tag_table


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

    def __repr__(self):
        return f'<Account - {self.name} (ID = {self.id})>'


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('user.id'))
    parent_id = Column(Integer, ForeignKey('category.id'), nullable=True)
    children = relationship('Category')

    name = Column(String)
    description = Column(String)

    creation_time = Column(String)
    modification_time = Column(String)
    is_actual = Column(Boolean)

    def __init__(self, id_user=0, parent_id=None, name='', description=''):
        if id_user:
            self.id_user = id_user
        elif current_user:
            self.id_user = current_user.get_id()
        self.parent_id = parent_id
        self.name = name
        self.description = description
        self.is_actual = 1
        self.creation_time = datetime.now()
        self.modification_time = None

    def add_form_data(self, data):
        self.name = data.name.data
        self.description = data.description.data
        self.parent_id = data.parent_id.data
        if self.id:
            self.modification_time = datetime.now()

    def __repr__(self):
        return f'<Category - {self.name} (ID = {self.id})>'


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('user.id'))

    name = Column(String)
    description = Column(String)
    operations = relationship(
        "Operation",
        secondary=operation_tag_table,
        back_populates="tags"
    )

    creation_time = Column(String)
    modification_time = Column(String)
    is_actual = Column(Boolean)

    def __init__(self, id_user=0, name='', description=''):
        if id_user:
            self.id_user = id_user
        elif current_user:
            self.id_user = current_user.get_id()
        self.name = name
        self.description = description
        self.is_actual = 1
        self.creation_time = datetime.now()
        self.modification_time = None

    def add_form_data(self, data):
        self.name = data.name.data
        self.description = data.description.data
        if self.id:
            self.modification_time = datetime.now()

    def __repr__(self):
        return f'<Tag: {self.id}, {self.name}>'


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