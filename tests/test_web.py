import pytest
from sqlalchemy.orm import sessionmaker
from web import app
from web.models import Account, Base, Category, Currency, User, Operation, Tag, create_engine

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


@pytest.fixture
def app():
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    with app.app_context():
        db = Base.metadata.create_all(engine)
        yield db
        Base.metadata.drop_all(engine)


# тест создания приложения
def test_app_creates(app):
    assert app
