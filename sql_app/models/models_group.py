from sqlalchemy import Table, Boolean, Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy_utils import EmailType, URLType
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
# from sqlalchemy.ext.declarative import declarative_/base

import datetime

from ..db.base_class import BaseCommons

# Base = declarative_base()


group_user_assoc = Table(
  'group_user_assoc',
  BaseCommons.metadata,
  Column('group_id', Integer, ForeignKey('groups.id')),
  Column('user_id', Integer, ForeignKey('users.id')),
)


class Group(BaseCommons):
  # __tablename__ = "Workspace"

  # __bind_key__ = 'DB_commons'

  ### meta
  id = Column(Integer, primary_key=True, index=True)
  created_date = Column(DateTime, default=datetime.datetime.utcnow)
  is_active = Column(Boolean, default=True)
  
  ### basic infos
  title = Column(String, index=True)
  description = Column(String, index=True)
  tags = Column(ARRAY(String), index=True, default=[])

  ### preferences
  color = Column(String, default='black')
  icon = Column(String, default='')

  ### access auths
  read = Column(String, default='owner-only')
  write = Column(String, default='owner-only')
  manage = Column(String, default='owner-only')
  invite = Column(String, default='owner-only')

  ### owner
  owner_id = Column(Integer, ForeignKey("users.id"))
  owner = relationship("User", backref="my_groups")

  ### relationships
  users = relationship(
    "User",
    secondary=group_user_assoc,
    backref="groups"
  )

  def can_manage(self, user_id: int):
    return self.owner_id == user_id
