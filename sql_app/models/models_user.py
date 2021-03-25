from . import ( Boolean, Column, Integer, String,
  EmailType, URLType,
  ForeignKey, relationship,
  DateTime, datetime
)

from ..db.base_class import Base

class User(Base):
  # __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)

  # email = Column(String, unique=True, index=True)
  email = Column(EmailType)
  # email = Column(String, unique=True, index=True, nullable=False)

  username = Column(String)
  name = Column(String)
  surname = Column(String)
  username = Column(String)
  description = Column(String)

  # image avatar
  avatar = Column(URLType)

  hashed_password = Column(String)

  created_date = Column(DateTime, default=datetime.datetime.utcnow)

  is_active = Column(Boolean, default=True)
  is_superuser = Column(Boolean, default=False)

  items = relationship("Item", back_populates="owner")
  posts = relationship("Post", back_populates="owner")
