print(">>>>>> import schemas_invitation.py >  Invitation ...")
from typing import List, Optional, Any
import datetime

from pydantic import BaseModel, EmailStr
# from uuid import UUID

from .schemas_choices import ItemType, InvitationStatus


class InvitationBase(BaseModel):
  ### basic infos
  title: str = "My invitation"
  message: Optional[str] = "My invitation message"

  ### linked data
  invitation_status: InvitationStatus = InvitationStatus.pending
  invitation_to_item_type: ItemType = ItemType.workspace
  invitation_to_item_id: int
  invitee: EmailStr

# print("=== SCH-schemas_invitation > InvitationBase : ", InvitationBase)


class InvitationCreate(InvitationBase):
  pass


class InvitationUpdate(InvitationBase):
  pass


class Invitation(InvitationBase):
  ### meta
  item_type: str = "invitation"
  id: int
  created_date: Optional[datetime.datetime]
  is_active: bool = True

  ### owner
  owner_id: int

  class Config:
    orm_mode = True


class InvitationList(Invitation):
  pass
  # owner: User
