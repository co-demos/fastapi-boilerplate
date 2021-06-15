print(">>>>>> import schemas_groups.py >  Group ...")
from typing import List, Optional, Any
import datetime

from pydantic import BaseModel, EmailStr
# from uuid import UUID

from .schemas_choices import PermissionType
# from .schemas_user import UserInDBBaseLight


class UserInDBBaseLight(BaseModel):
  ### meta
  item_type: str = "user"
  id: int = None
  email: EmailStr
  username: str = "Eli"
  name: Optional[str] = "Elinor"
  surname: Optional[str] = "Ostrom"
  locale: Optional[str] = "en"
  description: Optional[str] = "User description"
  class Config:
    orm_mode = True


class GroupBase(BaseModel):
  ### basic infos
  title: str = "My group"
  description: Optional[str] = "My group description"
  tags: Optional[List[str]] = []

  ### preferences
  color: Optional[str] = "black"
  icon: Optional[str] = "icon-users"

  ### access auths
  read: PermissionType = PermissionType.perm_owner
  write: PermissionType = PermissionType.perm_owner
  manage: PermissionType = PermissionType.perm_owner

  pending_users: Optional[List[EmailStr]] = []
  # pending_groups: Optional[List[int]] = []

  authorized_users: Optional[List[EmailStr]] = []
  # authorized_groups: Optional[List[int]] = []

# print("=== SCH-schemas_groups > GroupBase : ", GroupBase)


class GroupCreate(GroupBase):
  # users_pending: List[EmailStr] = []
  pending_users: List[EmailStr] = []


class GroupUpdate(GroupBase):
  users: List[UserInDBBaseLight] = []
  # users_pending: Optional[List[EmailStr]] = []
  pending_users: Optional[List[EmailStr]] = []


class Group(GroupUpdate):
  ### meta
  item_type: str = "group"
  id: int
  created_date: Optional[datetime.datetime]
  is_active: bool = True

  ### owner
  owner_id: int

  class Config:
    orm_mode = True


class GroupList(GroupBase):
  pass
  # owner: User


class GroupLight(GroupUpdate) :
  item_type: str = "group"
  id: int
  owner_id: int
  class Config:
    orm_mode = True

class GroupsList(BaseModel):
  __root__: List[GroupLight]
