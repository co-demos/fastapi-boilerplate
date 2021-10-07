# from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON
# from sqlalchemy_utils import EmailType, URLType
# from sqlalchemy.orm import relationship

# import datetime

# from ..db.base_class import BaseCommons

# class Post(BaseCommons):
#   # __tablename__ = "Posts"

#   # __bind_key__ = 'DB_commons'

#   id = Column(Integer, primary_key=True, index=True)
  
#   title = Column(String, index=True)
#   body = Column(String, index=True)

#   created_date = Column(DateTime, default=datetime.datetime.utcnow)
#   is_active = Column(Boolean, default=True)

#   owner_id = Column(Integer, ForeignKey("users.id"))
#   owner = relationship("User", back_populates="posts")

#   post_comments = relationship("Comment", back_populates="post_related")
