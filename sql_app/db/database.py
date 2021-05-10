print(">>>>>> import db.database.py ...")
import os
from ..core.config import settings

from typing import Any    
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta, declarative_base, as_declarative, declared_attr    
from sqlalchemy.orm import sessionmaker

from .base_class import BaseCommons, BaseData

### import databases

SQLALCHEMY_DATABASE_TYPE = settings.SQL_TYPE
# print("database.py > SQLALCHEMY_DATABASE_TYPE :", SQLALCHEMY_DATABASE_TYPE)

if SQLALCHEMY_DATABASE_TYPE == "sql_lite" :
  ### DB - COMMON TABLES
  SQLALCHEMY_DATABASE_URL = settings.SQLITE_DB_URL
  # DATABASE_URL = settings.SQLITE_DB_URL
  # print("database.py > sql_lite > SQLALCHEMY_DATABASE_URL :", SQLALCHEMY_DATABASE_URL)
  engine_commons = create_engine(SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} # only use with sqlite
  )

  ### DB - DYNAMIC DATA TABLES
  SQLALCHEMY_DATABASE_DATA_URL = settings.SQLITE_DB_DATA_URL
  # DATABASE_DATA_URL = settings.SQLITE_DB_DATA_URL
  # print("database.py > sql_lite > SQLALCHEMY_DATABASE_DATA_URL :", SQLALCHEMY_DATABASE_DATA_URL)
  engine_data = create_engine(SQLALCHEMY_DATABASE_DATA_URL,
    connect_args={"check_same_thread": False} # only use with sqlite
  )

elif SQLALCHEMY_DATABASE_TYPE == "postgre_sql" :
  ### DB - COMMON TABLES
  SQLALCHEMY_DATABASE_URL = settings.SQL_DB_URL
  # DATABASE_URL = settings.SQL_DB_URL_BIS
  print("database.py > postgre_sql > SQLALCHEMY_DATABASE_URL :", SQLALCHEMY_DATABASE_URL)
  engine_commons = create_engine(SQLALCHEMY_DATABASE_URL,
    pool_size=3,
    pool_pre_ping=True,
    max_overflow=0 # only use with postgresql
  )

  ### DB - DYNAMIC DATA TABLES
  SQLALCHEMY_DATABASE_URL_DATA = settings.SQL_DB_URL_DATA
  # DATABASE_URL_DATA = settings.SQL_DB_URL_DATA_BIS
  print("database.py > postgre_sql > SQLALCHEMY_DATABASE_URL_DATA :", SQLALCHEMY_DATABASE_URL_DATA)
  engine_data = create_engine(SQLALCHEMY_DATABASE_URL_DATA,
    pool_size=3,
    pool_pre_ping=True,
    max_overflow=0 # only use with postgresql
  )

### Create database if it does not exist.
if not database_exists(engine_commons.url):
  create_database(engine_commons.url)
if not database_exists(engine_data.url):
  create_database(engine_data.url)

# database = databases.Database(DATABASE_URL)

# SessionLocal = sessionmaker(
#   autocommit=False,
#   autoflush=False,
#   bind=engine_commons
# )


SessionLocal = sessionmaker(
  autocommit=False,
  autoflush=False,
)
SessionLocal.configure(binds={
    BaseCommons: engine_commons,
    BaseData: engine_data
  }
)


def get_db():
  # print("database.py > get_db > ... ")
  db = SessionLocal()
  # print("database.py > get_db > db :", db)
  try:
    yield db
  finally:
    db.close()
