from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, Boolean, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from web.db import Base


operation_tag_table = Table(
    'operation_tag',
    Base.metadata,
    Column('id_tag', Integer, ForeignKey('tag.id'), primary_key=True),
    Column('id_operation', Integer, ForeignKey('operation.id'), primary_key=True)
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
    creation_time = Column(DateTime, default=datetime.now())
    modification_time = Column(DateTime, default=None)
    is_actual = Column(Boolean, default=True)

    def __init__(self, id_cat=0, id_account=0, name='', description='', value=0, tags=[], date='', creation_type='web'):
        self.id_cat = id_cat
        self.id_account = id_account
        self.name = name
        self.description = description
        self.value = value
        self.tags = tags
        self.is_actual = True
        self.creation_type = creation_type
        if date:
            self.creation_time = date
        else:
            self.creation_time = datetime.now()
        self.modification_time = None

    def form_processing(self, form, tags_objects_list, id_operation=None):
        self.id_cat = form.id_cat.data
        self.id_account = form.id_account.data
        self.name = form.name.data
        self.description = form.description.data
        self.value = form.value.data
        self.creation_time = form.creation_time.data
        if tags_objects_list:
            self.tags = tags_objects_list
        if id_operation:
            self.modification_time = datetime.now()

    def __repr__(self):
        return f'<Operation: {self.id}, {self.name}>'
