import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from sqlalchemy import create_engine

from web.account.models import Account
from web.category.models import Category
from web.currency.models import Currency, Currency_Rate
from web.future_operation.models import FutureOperaion
from web.operation.models import Operation, operation_tag_table
from web.shared.models import SharedAccount, SharedOperaion, shared_acc_user_table
from web.tag.models import Tag
from web.user.models import User

from cfg import Config
from web.db import Base

if __name__ == '__main__':
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    Base.metadata.drop_all(engine)