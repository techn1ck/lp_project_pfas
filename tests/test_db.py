from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from cfg.web_settings import TestConfig, Config

engine = create_engine(TestConfig.SQLALCHEMY_DATABASE_URI)

session = scoped_session(sessionmaker(bind=engine))

""" Временный костыль для обеспечения работоспособности тестов
    Т.к. test_client почему-то подтягивает Config вместо TestConfig

    Разобраться почему на текущий момент не представляется возможным.
"""
Config.SQLALCHEMY_DATABASE_URI = TestConfig.SQLALCHEMY_DATABASE_URI
Config.WTF_CSRF_ENABLED = TestConfig.WTF_CSRF_ENABLED
Config.TESTING = TestConfig.TESTING
