from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from web import app

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))
