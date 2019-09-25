from ._service import *


shared_acc_user_table = Table('shared_acc_user', Base.metadata,
    Column('id_user', Integer, ForeignKey('user.id')),
    Column('id_shared_acc', Integer, ForeignKey('shared_account.id')),
    Column('user_ratio', Float)
)


class SharedAccount(Base):
    __tablename__ = 'shared_account'

    id = Column(Integer, primary_key=True)
    owner_id_user = Column(Integer, ForeignKey('user.id'))
#    id_currency = Column(Integer, ForeignKey('currency.id_currency'))
#    currency = relationship('Currency')

    name = Column(String)
    decscription = Column(String)

    creation_time = Column(String) 
    modification_time = Column(String)
    is_actual = Column(Boolean)

    users = relationship(
        "User",
        secondary=shared_acc_user_table,
        back_populates="shared_accounts")

    def __init__ (self):
        pass

    def __repr__ (self):
        return f'<SharedAccount: {self.id}, {self.name}>'


class SharedOperaion(Base):
    __tablename__ = 'shared_operation'

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('user.id'))
    id_shared_acc = Column(Integer, ForeignKey('category.id'))

    name = Column(String)
    decscription = Column(String)

    creation_time = Column(String) 
    modification_time = Column(String)
    is_actual = Column(Boolean)

    def __init__ (self):
        pass

    def __repr__ (self):
        return f'<SharedOperation: {self.id}, {self.name}>'



