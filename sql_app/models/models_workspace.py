from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy_utils import EmailType, URLType
from sqlalchemy.orm import relationship

import datetime

from ..db.base_class import Base

class Workspace(Base):
  # __tablename__ = "Workspace"

  ### meta
  id = Column(Integer, primary_key=True, index=True)
  created_date = Column(DateTime, default=datetime.datetime.utcnow)
  is_active = Column(Boolean, default=True)
  
  ### basic infos
  title = Column(String, index=True)
  description = Column(String, index=True)

  ### preferences
  color = Column(String, default='black')
  icon = Column(String, default='')

  ### access auths
  read = Column(String, default='owner-only')
  write = Column(String, default='owner-only')
  manage = Column(String, default='owner-only')

  ### owner
  owner_id = Column(Integer, ForeignKey("users.id"))
  owner = relationship("User", back_populates="my_workspaces")

  ### relationships
  datasets = Column(JSON)
  # datasets = relationship("Dataset", backref="parent")
  # sharing = relationship("User", back_populates="shared_workspaces")