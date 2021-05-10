from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy_utils import EmailType, URLType
from sqlalchemy.orm import relationship

import datetime

from ..db.base_class import BaseCommons

class Comment(BaseCommons):
  # __tablename__ = "comments"

  id = Column(Integer, primary_key=True, index=True)
  
  email = Column(EmailType)
  body = Column(String)
  comment_type = Column(String)

  created_date = Column(DateTime, default=datetime.datetime.utcnow)
  is_active = Column(Boolean, default=True)

  owner_id = Column(Integer, ForeignKey("users.id"))
  owner = relationship("User", back_populates="comments")

  post_id = Column(Integer, ForeignKey("posts.id"))
  post_related = relationship("Post", back_populates="post_comments")
