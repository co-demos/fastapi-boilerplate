from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy_utils import EmailType, URLType
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY

import datetime

from ..db.base_class import BaseCommons

import pprint
pp = pprint.PrettyPrinter(indent=1)


class Tablemeta(BaseCommons):
  # __tablename__ = "Tablemeta"

  # __bind_key__ = 'DB_commons'

  ### meta
  id = Column(Integer, primary_key=True, index=True)
  created_date = Column(DateTime, default=datetime.datetime.utcnow)
  is_active = Column(Boolean, default=True)
  
  ### basic infos
  title = Column(String, index=True)
  description = Column(String, index=True)
  licence = Column(String, index=True)
  tags = Column(ARRAY(String), index=True, default=[])
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

  pending_users = Column(ARRAY(EmailType), default=[])
  pending_groups = Column(ARRAY(Integer), default=[])

  authorized_users = Column(ARRAY(EmailType), default=[])
  authorized_groups = Column(ARRAY(Integer), default=[])

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

  def can_manage(self, user_id: int):
    return self.owner_id == user_id


# print("\n=== models_tablemeta > Tablemeta.__dict__ ...")
# pp.pprint(Tablemeta.__dict__)
