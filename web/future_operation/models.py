from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from web.db import Base


class FutureOperaion(Base):
    __tablename__ = 'future_operation'

    id = Column(Integer, primary_key=True)
    id_cat = Column(Integer, ForeignKey('category.id'))
    id_account = Column(Integer, ForeignKey('account.id'))

    name = Column(String)
    decscription = Column(String)

    creation_time = Column(String) 
    modification_time = Column(String)
    is_actual = Column(Boolean)

    def __init__ (self):
        pass

    def __repr__ (self):
        return f'<FutureOperation: {self.id}, {self.name}>'
