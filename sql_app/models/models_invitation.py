from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy_utils import EmailType, URLType
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import ARRAY

import datetime

from ..db.base_class import BaseCommons

class Invitation(BaseCommons):
  # __tablename__ = "Invitation"

  # __bind_key__ = 'DB_commons'

  ### meta
  id = Column(Integer, primary_key=True, index=True)
  created_date = Column(DateTime, default=datetime.datetime.utcnow)
  is_active = Column(Boolean, default=True)
  
  ### basic infos
  title = Column(String, index=True)
  message = Column(String, index=True)

  ### owner
  owner_id = Column(Integer, ForeignKey("users.id"))
  owner = relationship("User")
  # owner = relationship("User", back_populates="my_invitations")
  # owner = relationship("User", backref="my_invitations")
  # owner = relationship("User", backref=backref("invitations", uselist=False) )
  # owner = relationship("User", backref=backref("invitation", uselist=False) )

  ### invitation data
  invitation_to_item_type = Column(String)
  invitation_to_item_id = Column(Integer)
  invitation_status = Column(String, index=True) # pending | accepted | refused
  
  invitee = Column(EmailType)
  invitee_type = Column(String)
  invitee_id = Column(Integer)

  auths = Column(JSON)

  def can_manage(self, user_id: int):
    return self.owner_id == user_id
