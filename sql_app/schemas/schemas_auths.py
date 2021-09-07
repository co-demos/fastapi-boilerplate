print(">>>>>> import schemas_auths.py >  User ...")
from typing import List, Optional, Any
import datetime

from pydantic import BaseModel, EmailStr

from .schemas_choices import InviteeType, InvitationStatus


class AuthsInfosBasics(BaseModel): 
  ### access auths
  read: bool = False
  comment: bool = False
  patch: bool = False
  write: bool = False
  manage: bool = False


class AuthInfos(AuthsInfosBasics):
  ### meta
  invitee_type: InviteeType
  invitee_id: int = None
  # email: Optional[EmailStr]
  invitation_status: InvitationStatus

  created_date: Optional[datetime.datetime]
  accepted_date: Optional[datetime.datetime]

