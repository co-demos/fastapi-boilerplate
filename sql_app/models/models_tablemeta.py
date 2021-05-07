from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy_utils import EmailType, URLType
from sqlalchemy.orm import relationship

import datetime

from ..db.base_class import Base

import pprint
pp = pprint.PrettyPrinter(indent=1)


class Tablemeta(Base):
  # __tablename__ = "Tablemeta"

  ### meta
  id = Column(Integer, primary_key=True, index=True)
  created_date = Column(DateTime, default=datetime.datetime.utcnow)
  is_active = Column(Boolean, default=True)
  
  ### basic infos
  title = Column(String, index=True)
  description = Column(String, index=True)

  licence = Column(String, index=True)
  # schema = Column(String, index=True)

  ### preferences
  # color = Column(String, default='black')
  # icon = Column(String, default='')

  ### access auths
  read = Column(String, default='owner-only')
  comment = Column(String, default='owner-only')
  patch = Column(String, default='owner-only')
  write = Column(String, default='owner-only')
  manage = Column(String, default='owner-only')

  ### owner
  owner_id = Column(Integer, ForeignKey("users.id"))
  # owner = relationship("User", back_populates="my_tables")

  ### relationships
  dataset_id = Column(Integer, ForeignKey("datasets.id"))
  dataset_related = relationship("Dataset", back_populates="tables")

  ### table data
  table_fields = Column(JSON)
  # table_data = Column(String, index=True)
  table_data_uuid = Column(String, index=True)

  # sharing = relationship("User", back_populates="shared_tables")

# print("\n=== models_tablemeta > Tablemeta.__dict__ ...")
# pp.pprint(Tablemeta.__dict__)
