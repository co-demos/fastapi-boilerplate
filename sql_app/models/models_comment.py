from . import ( Boolean, Column, Integer, String,
  EmailType,
  ForeignKey, relationship,
  DateTime, datetime
)

from ..db.base_class import Base

class Comment(Base):
  # __tablename__ = "Comments"

  id = Column(Integer, primary_key=True, index=True)
  
  email = Column(EmailType)
  body = Column(String)

  created_date = Column(DateTime, default=datetime.datetime.utcnow)
  is_active = Column(Boolean, default=True)

  owner_id = Column(Integer, ForeignKey("users.id"))
  owner = relationship("User", back_populates="comments")

  post_id = Column(Integer, ForeignKey("posts.id"))
  post_related = relationship("Post", back_populates="post_comments")
