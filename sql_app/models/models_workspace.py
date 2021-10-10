from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy_utils import EmailType, URLType
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY, JSONB

import datetime

from ..db.base_class import BaseCommons

class Workspace(BaseCommons):
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
  comment = Column(String, default='owner-only')
  write = Column(String, default='owner-only')
  manage = Column(String, default='owner-only')

  # pending_users = Column(ARRAY(EmailType), default=[])
  # pending_groups = Column(ARRAY(Integer), default=[])
  # authorized_users = Column(ARRAY(EmailType), default=[])
  # authorized_groups = Column(ARRAY(Integer), default=[])

  # pending_users = Column(ARRAY(JSONB), default=[])
  # pending_groups = Column(ARRAY(JSONB), default=[])
  # authorized_users = Column(ARRAY(JSONB), default=[])
  # authorized_groups = Column(ARRAY(JSONB), default=[])

  # pending_users = Column(JSONB, default=[])
  # pending_groups = Column(JSONB, default=[])
  # authorized_users = Column(JSONB, default=[])
  # authorized_groups = Column(JSONB, default=[])

  pending_users = Column(JSONB)
  pending_groups = Column(JSONB)
  authorized_users = Column(JSONB)
  authorized_groups = Column(JSONB)

  ### owner
  owner_id = Column(Integer, ForeignKey("users.id"))
  # owner = relationship("User", back_populates="my_workspaces")
  owner = relationship("User", backref="my_workspaces")

  ### relationships
  datasets = Column(JSON)
  # datasets = relationship("Dataset", backref="parent")
  # sharing = relationship("User", back_populates="shared_workspaces")

  def can_manage(self, user_id: int):
    return self.owner_id == user_id
