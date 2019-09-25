from ._service import *


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('user.id'))
#    id_currency = Column(Integer, ForeignKey('currency.id'))
#    currency = relationship('Currency')

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
