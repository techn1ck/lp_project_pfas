from ._service import *
from .shared import shared_acc_user_table

class User(Base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    telegram = Column(String, unique=True)
    name = Column(String)
    surname = Column(String)
    password = Column(String(128))
    phone = Column(BigInteger, unique=True)
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

    def __init__ (self, telegram, name, surname, password, phone, email, role, creation_time, modification_time=None, is_actual=1):
        self.telegram = telegram
        self.name = name
        self.surname = surname
        self.password = password
        self.phone = phone
        self.email = email
        self.role = role
        self.creation_time = creation_time
        self.modification_time = modification_time
        self.is_actual = is_actual

    def __repr__ (self):
        return f'<User: {self.name} (ID = {self.id}, telegram = {self.telegram})>'
# import where you call: from werkzeug.security import generate_password_hash, check_password_hash
    # def set_password(self, password):
    #     self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)