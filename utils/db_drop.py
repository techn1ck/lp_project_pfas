import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from classes import *

if __name__ == '__main__':
    engine = create_engine('postgresql+psycopg2://test2:111@localhost:5432/test2')
    Base.metadata.drop_all(engine)