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
    
    creation_time = Column(String)
    modification_time = Column(String)
    is_actual = Column(Boolean)

    shared_accounts = relationship(
        "SharedAccount",
        secondary=shared_acc_user_table,
        back_populates="users")
    
    accounts = relationship('Account')
    categories = relationship('Category')
    default_currency = Column(Integer, ForeignKey('currency.id'), unique=True)

    def __init__ (self):
        pass

    def __repr__ (self):
        return f'<User: {self.id}, {self.telegram}>'
