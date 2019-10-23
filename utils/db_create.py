import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from sqlalchemy import create_engine

from cfg.web_settings import Config
from web.db import Base, engine


if __name__ == '__main__':
    Base.metadata.create_all(engine)