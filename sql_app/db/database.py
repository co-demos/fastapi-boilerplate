import os
from typing import Any    
from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta, declarative_base, as_declarative, declared_attr    
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_TYPE = os.getenv("SQL_TYPE")

if SQLALCHEMY_DATABASE_TYPE == "sql_lite" :
  SQLALCHEMY_DATABASE_URL = os.getenv("SQLITE_DB_URL")
  engine = create_engine(SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} # only use with sqlite
  )

elif SQLALCHEMY_DATABASE_TYPE == "postgre_sql" :
  SQLALCHEMY_DATABASE_URL = os.getenv("SQL_DB_URL")
  engine = create_engine(SQLALCHEMY_DATABASE_URL,
    pool_size=3, max_overflow=0 # only use with postgresql
  )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
