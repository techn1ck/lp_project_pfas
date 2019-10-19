from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from web import app

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Base = declarative_base()

session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))
