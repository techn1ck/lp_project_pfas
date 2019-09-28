from ._service import *
from .operation_class import operation_tag_table


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('user.id'))
    id_currency = Column(Integer, ForeignKey('currency.id'))
    currency = relationship('Currency')

    name = Column(String)
    decscription = Column(String)

    creation_time = Column(String) 
    modification_time = Column(String)
    is_actual = Column(Boolean)

    def __init__ (self):
        pass

    def __repr__ (self):
        return f'<Account: {self.id}, {self.name}>'


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('user.id'))
    parent_id_cat = Column(Integer, ForeignKey('category.id'))
    sub_categories = relationship('Category')

    name = Column(String)
    decscription = Column(String)

    creation_time = Column(String) 
    modification_time = Column(String)
    is_actual = Column(Boolean)


    def __init__ (self):
        pass

    def __repr__ (self):
        return f'<Category: {self.id}, {self.name}>'


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('user.id'))
    
    name = Column(String)
    decscription = Column(String)
    operations = relationship(
        "Operation",
        secondary=operation_tag_table,
        back_populates="tags"
    )
    
    creation_time = Column(String)
    modification_time = Column(String)
    is_actual = Column(Boolean)

    def __init__ (self):
        pass

    def __repr__ (self):
        return f'<Tag: {self.id}, {self.name}>'


class Currency(Base):
    __tablename__ = 'currency'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    short_name = Column(String)
    symbol = Column(String(2)) # длина в байтах или в символах? пишут, что зависит от БД

    def __init__ (self):
        pass

    def __repr__ (self):
        return f'<Currency: {self.id_currency}, {self.name}>'


class Currency_Rate(Base):
    __tablename__ = 'currency_rate'

    id = Column(Integer, primary_key=True)

    id_account = Column(Integer, ForeignKey('account.id'))
    id_account_currency = relationship("Account", foreign_keys="Account.id_currency")
    id_default_currency = relationship("User", foreign_keys="User.id_currency")

    rate  = Column(Numeric)
    operation_date = Column(String) # TIMESTAMP?

    def __init__ (self):
        pass

    def __repr__ (self):
        return f'<Currency rate: {currency.name}, {self.value}>'