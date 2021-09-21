from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy_utils import EmailType, URLType
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY, JSONB

import datetime

from ..db.base_class import BaseCommons

class Dataset(BaseCommons):
  # __tablename__ = "datasets"

  ### meta
  id = Column(Integer, primary_key=True, index=True)
  created_date = Column(DateTime, default=datetime.datetime.utcnow)
  is_active = Column(Boolean, default=True)
  
  ### basic infos
  title = Column(String, index=True)
  description = Column(String, index=True)
  licence = Column(String, index=True)
  tags = Column(ARRAY(String), index=True, default=[])

  ### preferences
  color = Column(String, default='black')
  icon = Column(String, default='')

  ### access auths
  read = Column(String, default='owner-only')
  comment = Column(String, default='owner-only')
  patch = Column(String, default='owner-only')
  write = Column(String, default='owner-only')
  manage = Column(String, default='owner-only')

  # pending_users = Column(ARRAY(EmailType), default=[])
  # pending_groups = Column(ARRAY(Integer), default=[])
  # authorized_users = Column(ARRAY(EmailType), default=[])
  # authorized_groups = Column(ARRAY(Integer), default=[])

  # pending_users = Column(ARRAY(JSON), default=[])
  # pending_groups = Column(ARRAY(JSON), default=[])
  # authorized_users = Column(ARRAY(JSON), default=[])
  # authorized_groups = Column(ARRAY(JSON), default=[])

  pending_users = Column(JSONB)
  pending_groups = Column(JSONB)
  authorized_users = Column(JSONB)
  authorized_groups = Column(JSONB)

  ### foreign keys
  owner_id = Column(Integer, ForeignKey("users.id"))
  # owner = relationship("User", back_populates="my_datasets")
  owner = relationship("User", backref="my_datasets")

  # workspace_related = relationship("Workspace", back_populates="datasets")
  # workspace_id = Column(Integer, ForeignKey('workspace.id'))
  
  ### relationships
  tables = relationship("Tablemeta", back_populates="dataset_related")
  
  # sharing = relationship("User", back_populates="shared_workspaces")
  
  ### UX preferences
  ux_tables = Column(JSON)

  def can_manage(self, user_id: int):
    return self.owner_id == user_id
