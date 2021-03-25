from typing import Any    

import inflect   

# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta, declarative_base, as_declarative, declared_attr    

p = inflect.engine()    

# Base = declarative_base()
# Base: DeclarativeMeta = declarative_base()
@as_declarative()
class Base:
  id: Any
  __name__: str
  # Generate __tablename__ automatically
  @declared_attr    
  def __tablename__(cls):    
    return p.plural(cls.__name__.lower())