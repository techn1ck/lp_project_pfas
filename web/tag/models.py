from datetime import datetime
from flask_login import current_user

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from web.db import Base
from web.operation.models import operation_tag_table


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('user.id'))

    name = Column(String)
    description = Column(String)
    operations = relationship(
        "Operation",
        secondary=operation_tag_table,
        back_populates="tags"
    )

    creation_time = Column(String)
    modification_time = Column(String)
    is_actual = Column(Boolean)

    def __init__(self, id_user=0, name='', description=''):
        if id_user:
            self.id_user = id_user
        elif current_user:
            self.id_user = current_user.get_id()
        self.name = name
        self.description = description
        self.is_actual = 1
        self.creation_time = datetime.now()
        self.modification_time = None

    def add_form_data(self, data):
        self.name = data.name.data
        self.description = data.description.data
        if self.id:
            self.modification_time = datetime.now()

    def __repr__(self):
        return f'<Tag: {self.id}, {self.name}>'
