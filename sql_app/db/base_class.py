print(">>>>>> import db.base_class.py ...")
from typing import Any    

import inflect   

from sqlalchemy import Table
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import ( 
  declarative_base, 
  DeclarativeMeta, 
  as_declarative, 
  declared_attr 
)
from sqlalchemy.ext.automap import automap_base

p = inflect.engine()

@as_declarative()
class BaseCommons:
  id: Any
  __name__: str

  # Generate __tablename__ automatically
  @declared_attr
  def __tablename__(cls):
    return p.plural(cls.__name__.lower())

  @declared_attr
  def __bind_key__(cls):
    return "DB_commons"


# BaseData = automap_base()
BaseData = declarative_base()
# class BaseData(object):
#   @classmethod
#   def __table_cls__(cls, *args, **kwargs):
#     t = Table(*args, **kwargs)
#     t.__decl_class__ = cls
#     return t
# BaseData = declarative_base(cls=BaseData)
