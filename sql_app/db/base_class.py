print(">>>>>> import db.base_class.py ...")
from typing import Any    

import inflect   

# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import ( 
  declarative_base, 
  DeclarativeMeta, 
  as_declarative, 
  declared_attr 
)

p = inflect.engine()

@as_declarative()
class Base:
  id: Any
  __name__: str
  # Generate __tablename__ automatically
  @declared_attr
  def __tablename__(cls):
    return p.plural(cls.__name__.lower())
