from . import ( Boolean, Column, Integer, String,
  ForeignKey, relationship,
  DateTime, datetime
)

from ..db.base_class import Base

class Post(Base):
  # __tablename__ = "Posts"

  id = Column(Integer, primary_key=True, index=True)
  
  title = Column(String, index=True)
  body = Column(String, index=True)

  created_date = Column(DateTime, default=datetime.datetime.utcnow)
  is_active = Column(Boolean, default=True)

  owner_id = Column(Integer, ForeignKey("users.id"))
  owner = relationship("User", back_populates="posts")
