from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from cfg.web_settings import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Base = declarative_base()

session = scoped_session(sessionmaker(bind=engine))
