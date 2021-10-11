from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy_utils import EmailType, URLType
from sqlalchemy.orm import relationship

import datetime

from ..db.base_class import BaseCommons

class Comment(BaseCommons):
  # __tablename__ = "comments"

  ### meta
  id = Column(Integer, primary_key=True, index=True)
  created_date = Column(DateTime, default=datetime.datetime.utcnow)
  is_active = Column(Boolean, default=True)

  ### basic infos
  # title = Column(String, index=True)
  message = Column(String, index=True)

  ### owner (as optional to include not registred users)
  owner_email = Column(EmailType)
  # owner_email = Column(String, ForeignKey("users.email"))
  # owner_id = Column(Integer, ForeignKey("users.id"))
  # owner = relationship("User")
  alert_item_owner = Column(Boolean, default=False)

  ### comment data 
  comment_to_item_type = Column(String, index=True)
  comment_to_item_id = Column(Integer, index=True)
  comment_status = Column(String, index=True) # new | read | treated | inappropriate

  response_to_comment_id = Column(Integer, index=True)

  ### related patch
  # has_patch = Column(Boolean)
  patch_id = Column(Integer, ForeignKey("patches.id"))
  patch = relationship("Patch")

