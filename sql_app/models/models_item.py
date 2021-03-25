from . import Boolean, Column, ForeignKey, Integer, String, \
  relationship, \
  DateTime, datetime

from ..db.base_class import Base

class Item(Base):
  # __tablename__ = "items"

  id = Column(Integer, primary_key=True, index=True)
  
  title = Column(String, index=True)
  description = Column(String, index=True)

  created_date = Column(DateTime, default=datetime.datetime.utcnow)

  # owner_id = Column(Integer, ForeignKey("users.id"))
  # owner = relationship("User", back_populates="items")
