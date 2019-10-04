from datetime import datetime, date
from flask_login import UserMixin

from sqlalchemy import create_engine, Table, Column, Integer, String, Float, Boolean, Numeric, Date, DateTime, BigInteger, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.ext.declarative import declarative_base

from werkzeug.security import check_password_hash

from web import ID_USER

Base = declarative_base()