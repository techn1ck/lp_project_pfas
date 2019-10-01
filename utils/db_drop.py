import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from web.models import *
from cfg import DB_STRING

if __name__ == '__main__':
    engine = create_engine(DB_STRING, echo=True)
    Base.metadata.drop_all(engine)