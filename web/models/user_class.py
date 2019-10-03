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
    password = Column(String)

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

    def __init__ (self, name='', telegram='', email='', phone=0, id=0):
        self.name = name
        self.telegram = telegram
        self.role = 'user' 
        self.email = email
        self.phone = phone
        self.is_actual = 1
        #if not self.id and id:
            #self.id = id

    def __repr__ (self):
        return f'<User: {self.name} (ID = {self.id}, telegram = {self.telegram})>'
