import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from web.db import Base, session


if __name__ == '__main__':
    for table in reversed(Base.metadata.sorted_tables):
        print(f"Clear table - {table}")
        session.execute(table.delete())
    session.commit()
