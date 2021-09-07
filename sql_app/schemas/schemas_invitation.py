print(">>>>>> import schemas_invitation.py >  Invitation ...")
from typing import List, Optional, Any
import datetime

from pydantic import BaseModel, EmailStr
# from uuid import UUID

from .schemas_choices import ItemType, InvitationStatus, InviteeType
from .schemas_auths import AuthsInfosBasics


class Invitee(BaseModel):
  invitee_type: InviteeType = InviteeType.user
  invitee_email: Optional[EmailStr]
  invitee_id: Optional[int]


class InvitationBasics(BaseModel):
  ### basic infos
  message_title: Optional[str] = "My invitation title"
  message: Optional[str] = "My invitation message"

  ### linked data
  # invitor_id: int
  invitation_to_item_id: int
  invitees: Optional[List[Invitee]] = []

  # auth levels
  auths: Optional[AuthsInfosBasics]

class InvitationToGroup(InvitationBasics):
  invitation_to_item_type: ItemType = ItemType.group

class InvitationToWorkspace(InvitationBasics):
  invitation_to_item_type: ItemType = ItemType.workspace

class InvitationToDataset(InvitationBasics):
  invitation_to_item_type: ItemType = ItemType.dataset

class InvitationToTablemeta(InvitationBasics):
  invitation_to_item_type: ItemType = ItemType.table


class InvitationBase(BaseModel):
  ### basic infos
  title: str = "My invitation"
  # message_title: Optional[str] = "My invitation title"
  message: Optional[str] = "My invitation message"

  ### linked data
  invitation_status: InvitationStatus = InvitationStatus.pending
  invitation_to_item_type: ItemType = ItemType.workspace
  invitation_to_item_id: int
  invitee: EmailStr

  # auth levels
  auths: Optional[AuthsInfosBasics]

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
