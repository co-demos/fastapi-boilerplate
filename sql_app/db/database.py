print(">>>>>> import db.database.py ...")
import os
from ..core.config import settings

from typing import Any    
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta, declarative_base, as_declarative, declared_attr    
from sqlalchemy.orm import sessionmaker

import databases

SQLALCHEMY_DATABASE_TYPE = settings.SQL_TYPE
# print("database.py > SQLALCHEMY_DATABASE_TYPE :", SQLALCHEMY_DATABASE_TYPE)

if SQLALCHEMY_DATABASE_TYPE == "sql_lite" :
  SQLALCHEMY_DATABASE_URL = settings.SQLITE_DB_URL
  DATABASE_URL = settings.SQLITE_DB_URL
  # print("database.py > sql_lite > SQLALCHEMY_DATABASE_URL :", SQLALCHEMY_DATABASE_URL)
  engine = create_engine(SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} # only use with sqlite
  )

elif SQLALCHEMY_DATABASE_TYPE == "postgre_sql" :
  SQLALCHEMY_DATABASE_URL = settings.SQL_DB_URL
  DATABASE_URL = settings.SQL_DB_URL_BIS
  # print("database.py > postgre_sql > SQLALCHEMY_DATABASE_URL :", SQLALCHEMY_DATABASE_URL)
  engine = create_engine(SQLALCHEMY_DATABASE_URL,
    pool_size=3,
    pool_pre_ping=True,
    max_overflow=0 # only use with postgresql
  )

database = databases.Database(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
