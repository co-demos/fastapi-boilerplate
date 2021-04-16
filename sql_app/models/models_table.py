from . import ( Boolean, Column, Integer, String,
  ForeignKey, relationship,
  DateTime, datetime
)

from ..db.base_class import Base

class Table(Base):
  # __tablename__ = "Table"

  ### meta
  id = Column(Integer, primary_key=True, index=True)
  created_date = Column(DateTime, default=datetime.datetime.utcnow)
  is_active = Column(Boolean, default=True)
  
  ### basic infos
  title = Column(String, index=True)
  description = Column(String, index=True)

  # licence = Column(String, index=True)
  # schema = Column(String, index=True)

  ### preferences
  color = Column(String, default='black')
  icon = Column(String, default='')

  ### access auths
  read = Column(String, default='owner-only')
  comment = Column(String, default='owner-only')
  patch = Column(String, default='owner-only')
  write = Column(String, default='owner-only')
  manage = Column(String, default='owner-only')

  ### owner
  owner_id = Column(Integer, ForeignKey("users.id"))
  dataset_id = Column(Integer, ForeignKey("datasets.id"))
  # owner = relationship("User", back_populates="my_tables")

  ### relationships
  # table_data = relationship("TableData", back_populates="table_related")
  # sharing = relationship("User", back_populates="shared_tables")
