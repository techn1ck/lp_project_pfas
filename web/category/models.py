from datetime import datetime
from flask_login import current_user

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from web.db import Base


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('user.id'))
    parent_id = Column(Integer, ForeignKey('category.id'), nullable=True)
    children = relationship('Category')

    name = Column(String)
    description = Column(String)

    creation_time = Column(String)
    modification_time = Column(String)
    is_actual = Column(Boolean)

    def __init__(self, id_user=0, parent_id=None, name='', description=''):
        if id_user:
            self.id_user = id_user
        elif current_user:
            self.id_user = current_user.get_id()
        self.parent_id = parent_id
        self.name = name
        self.description = description
        self.is_actual = 1
        self.creation_time = datetime.now()
        self.modification_time = None

    def add_form_data(self, data):
        self.name = data.name.data
        self.description = data.description.data
        self.parent_id = data.parent_id.data
        if self.id:
            self.modification_time = datetime.now()

    def invert_is_actual(self):
        if self.is_actual:
            self.is_actual = False
        else:
            self.is_actual = True

    def __repr__(self):
        return f'<Category - {self.name} (ID = {self.id})>'
