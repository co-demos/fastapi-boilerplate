from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy_utils import EmailType, URLType
from sqlalchemy.orm import relationship

import datetime

from ..db.base_class import BaseCommons

class Licence(BaseCommons):
  # __tablename__ = "Licence"

  # __bind_key__ = 'DB_commons'

  ### meta
  id = Column(Integer, primary_key=True, index=True)
  created_date = Column(DateTime, default=datetime.datetime.utcnow)
  is_active = Column(Boolean, default=True)
  
  ### basic infos
  title = Column(String, index=True, unique=True,)
  fullname = Column(String, index=True)
  category = Column(String)
  url = Column(String)

  # name: The name MUST be an Open Definition license ID(opens new window)
  # path: A url-or-path string, that is a fully qualified HTTP address, or a relative POSIX path (see the url-or-path definition in Data Resource for details).
  # title: A human-readable title.
