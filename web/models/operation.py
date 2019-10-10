from ._service import *

operation_tag_table = Table('operation_tag', Base.metadata,
    Column('id_tag', Integer, ForeignKey('tag.id')),
    Column('id_operation', Integer, ForeignKey('operation.id'))
)

class Operation(Base):
    __tablename__ = 'operation'

    id = Column(Integer, primary_key=True)
    id_cat = Column(Integer, ForeignKey('category.id'))
    id_account = Column(Integer, ForeignKey('account.id'))
    id_shared_operation = Column(Integer, ForeignKey('shared_operation.id'), default=None)
    id_future_operation = Column(Integer, ForeignKey('future_operation.id'), default=None)

    name = Column(String)
    description = Column(String, default=None)
    value = Column(Numeric)
    tags = relationship(
        "Tag",
        secondary=operation_tag_table,
        back_populates="operations"
    )

    creation_type = Column(String, default="web")  # web, bot, parser, shared
    creator_id_user = Column(Integer, ForeignKey('user.id'), default=None)  # for shared operations
    creation_time = Column(DateTime, default = datetime.now())
    modification_time = Column(DateTime, default=None)
    is_actual = Column(Boolean, default=True)

    def __init__(self, id_cat, id_account, name, description, value):
        self.id_cat = id_cat
        self.id_account = id_account
        # self.id_shared_operation = id_shared_operation
        # self.id_future_operation = id_future_operation
        self.name = name
        self.description = description
        self.value = value
        # self.creation_type = creation_type
        # self.creator_id_user = creator_id_user
        # self.creation_time = creation_time
        # self.modification_time = modification_time
        # self.is_actual = is_actual

    def __repr__ (self):
        return f'<Operation: {self.id}, {self.name}>'
