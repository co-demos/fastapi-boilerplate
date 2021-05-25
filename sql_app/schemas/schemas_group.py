print(">>>>>> import schemas_groups.py >  Group ...")
from typing import List, Optional, Any
import datetime

from pydantic import BaseModel, EmailStr
# from uuid import UUID

from .schemas_permissions import PermissionType
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

  ### linked data
  users: List[UserInDBBaseLight] = []


# print("=== SCH-schemas_groups > GroupBase : ", GroupBase)


class GroupCreate(GroupBase):
  pass


class GroupUpdate(GroupBase):
  pass


class Group(GroupBase):
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

