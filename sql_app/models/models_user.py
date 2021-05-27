from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy_utils import EmailType, URLType
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY

import datetime

from ..db.base_class import BaseCommons

from .models_group import group_user_assoc


class User(BaseCommons):
  # __tablename__ = "users"

  # __bind_key__ = 'DB_commons'

  ### meta
  id = Column(Integer, primary_key=True, index=True)
  created_date = Column(DateTime, default=datetime.datetime.utcnow)
  modif_date = Column(DateTime, default=datetime.datetime.utcnow)

  ### basic infos
  # email = Column(String, unique=True, index=True)
  # email = Column(String, unique=True, index=True, nullable=False)
  email = Column(EmailType)
  username = Column(String)
  name = Column(String)
  surname = Column(String)
  username = Column(String)
  description = Column(String)
  locale = Column(String)

  ### preferences
  avatar_url = Column(URLType)

  ### security
  hashed_password = Column(String)
  is_active = Column(Boolean, default=True)
  is_superuser = Column(Boolean, default=False)

  ### relationships
  items = relationship("Item", back_populates="owner")
  posts = relationship("Post", back_populates="owner")
  comments = relationship("Comment", back_populates="owner")

  ### relationships / data patch items
  my_workspaces = relationship("Workspace", back_populates="owner")
  my_datasets = relationship("Dataset", back_populates="owner")
  # my_tables = relationship("Table", back_populates="owner")
  # my_schemas = relationship("Schema", back_populates="owner")
  # my_fields = relationship("SchemaField", back_populates="owner")

  # my_groups = relationship("Group", back_populates="owner")

  # my_invitations = relationship("Invitation", back_populates="owner")
  # my_notifications = relationship("Invitation")

  # shared_workspaces = relationship("Workspace", back_populates="sharing")
  # shared_datasets = relationship("Dataset", back_populates="sharing")
  # shared_tables = relationship("Table", back_populates="sharing")
  # shared_schemas = relationship("Schema", back_populates="sharing")
  # shared_fields = relationship("SchemaField", back_populates="sharing")

  ### UX preferences
  ux_workspaces = Column(JSON)
  ux_groups = Column(JSON)
  # ux_datasets = Column(JSON)


  def can_manage(self, user_id: int):
    return self.owner_id == user_id
