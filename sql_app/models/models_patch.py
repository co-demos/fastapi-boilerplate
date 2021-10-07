from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy_utils import EmailType, URLType
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import ARRAY, JSONB

import datetime

from ..db.base_class import BaseCommons

class Patch(BaseCommons):
  # __tablename__ = "Patch"

  # __bind_key__ = 'DB_commons'

  ### meta
  id = Column(Integer, primary_key=True, index=True)
  created_date = Column(DateTime, default=datetime.datetime.utcnow)
  is_active = Column(Boolean, default=True)
  
  ### basic infos
  # title = Column(String, index=True)
  message = Column(String, index=True)

  ### owner
  # owner_email = Column(String, ForeignKey("users.email"))
  # owner_id = Column(Integer, ForeignKey("users.id"))
  # owner = relationship("User")

  ### patch data
  patch_type = Column(String)
  patch_to_item_type = Column(String)
  patch_to_item_id = Column(Integer)
  patch_status = Column(String, index=True) # pending | accepted | modified | refused
  patch_data = Column(JSONB)

  def can_manage(self, user_id: int):
    return self.owner_id == user_id
