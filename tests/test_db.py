import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from cfg import TestConfig

engine = create_engine(TestConfig.SQLALCHEMY_DATABASE_URI)

session = scoped_session(sessionmaker(bind=engine))
