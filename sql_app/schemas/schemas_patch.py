print(">>>>>> import schemas_patch.py >  Patch ...")
from typing import List, Optional, Any
import datetime

from pydantic import BaseModel, EmailStr
# from uuid import UUID

from .schemas_choices import ItemType, PatchStatus, InviteeType, PatchStatusAction
# from .schemas_auths import AuthsInfosBasics

# from .schemas_user import User, UserInDBBaseLight



class PatchBasics(BaseModel):
  ### basic infos
  # title: Optional[str] = "My patch title"
  # message: Optional[str] = "My patch message"

  ### linked data
  # invitor_id: int
  patch_to_item_id: int

  # auth levels
  # auths: Optional[AuthsInfosBasics]

# class PatchToGroup(PatchBasics):
#   patch_to_item_type: ItemType = ItemType.group

# class PatchToWorkspace(PatchBasics):
#   patch_to_item_type: ItemType = ItemType.workspace

# class PatchToDataset(PatchBasics):
#   patch_to_item_type: ItemType = ItemType.dataset

# class PatchToTablemeta(PatchBasics):
#   patch_to_item_type: ItemType = ItemType.table


# class PatchResponse(BaseModel):
#   ### basic infos
#   patch_id: int
#   action: PatchStatusAction


class PatchBase(BaseModel):
  ### basic infos
  # title: str = "My patch"
  # message_title: Optional[str] = "My patch title"
  message: Optional[str] = "My patch message"

  ### linked data
  patch_status: PatchStatus = PatchStatus.pending
  patch_to_item_type: ItemType = ItemType.workspace
  patch_to_item_id: int

  invitee: EmailStr
  invitee_type: Optional[str]
  invitee_id: Optional[int]

  # auth levels
  auths: Optional[AuthsInfosBasics]

# print("=== SCH-schemas_patch > PatchBase : ", PatchBase)


class PatchCreate(PatchBase):
  pass


class PatchUpdate(PatchBase):
  pass


class Patch(PatchBase):
  ### meta
  item_type: str = "patch"
  id: int
  created_date: Optional[datetime.datetime]
  is_active: bool = True

  ### owner
  # owner_id: int
  # owner: UserInDBBaseLight

  class Config:
    orm_mode = True


class PatchList(Patch):
  pass
  # owner: User
