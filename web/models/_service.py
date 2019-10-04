from datetime import datetime, date
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.ext.declarative import declarative_base

from web import ID_USER

Base = declarative_base()