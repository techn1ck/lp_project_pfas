from ._service import *

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

    def form_processing(self, form, tags_objects_list, id_operation=None):
        self.id_cat = form.category.data
        self.id_account = form.account.data
        self.name = form.name.data
        self.description = form.description.data
        self.value = form.value.data
        if tags_objects_list:
            self.tags = tags_objects_list
        if id_operation:
            self.modification_time = datetime.now()

    def __init__(self):
        pass

    def __repr__(self):
        return f'<Operation: {self.id}, {self.name}>'
