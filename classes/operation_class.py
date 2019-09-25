from ._service import *


class Operation(Base):
    __tablename__ = 'operation'

    id = Column(Integer, primary_key=True)
    id_cat = Column(Integer, ForeignKey('category.id'))
    id_account = Column(Integer, ForeignKey('account.id'))
    id_shared_operation = Column(Integer, ForeignKey('shared_operation.id'))
    id_future_operation = Column(Integer, ForeignKey('future_operation.id'))

    name = Column(String)
    description = Column(String)

    creation_type = Column(String) # web, bot, parser, shared
    creator_id_user = Column(Integer, ForeignKey('user.id')) # for shared operations

    creation_time = Column(String) 
    modification_time = Column(String)
    is_actual = Column(Boolean)
    
    def __init__ (self):
        pass

    def __repr__ (self):
        return f'<Operation: {self.id}, {self.telegram}>'
