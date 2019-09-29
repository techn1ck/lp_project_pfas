from ._service import *
from .operation_class import operation_tag_table


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('user.id'))
#    id_currency = Column(Integer, ForeignKey('currency.id'))
#    currency = relationship('Currency')

    name = Column(String)
    description = Column(String)

    creation_time = Column(String) 
    modification_time = Column(String)
    is_actual = Column(Boolean)

    def __init__ (self):
        pass

    def __repr__ (self):
        return f'<Account: {self.id}, {self.name}>'

    def get_form_fields(self):
        return {
            "id_account" : 1,
            "name" : 2,
            "description" : 3,
        }


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
