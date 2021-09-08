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


class UserAuthPending(BaseModel):
  invitation_id: int
  # invitation_status: str = None
  user_id: Optional[int] = None
  user_email: str = None


class GroupAuthPending(BaseModel):
  invitation_id: int
  # invitation_status: str = None
  group_id: int = None


class UserAuthInfos(AuthsInfosBasics):
  user_id: Optional[int] = None
  user_email: str = None


class GroupAuthInfos(AuthsInfosBasics):
  group_id: int = None
