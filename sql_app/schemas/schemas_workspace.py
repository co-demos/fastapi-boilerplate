print(">>>>>> import schemas_workspace.py >  Workspace ...")
from typing import List, Optional, Any
import datetime

from pydantic import BaseModel, EmailStr
# from uuid import UUID

from .schemas_dataset import Dataset
from .schemas_choices import PermissionType


class WorkspaceBase(BaseModel):
  ### basic infos
  title: str = "My workspace"
  description: Optional[str] = "My workspace description"
  tags: Optional[List[str]] = []

  ### preferences
  color: Optional[str] = "black"
  icon: Optional[str] = "icon-database"

  ### access auths
  read: PermissionType = PermissionType.perm_owner
  comment: PermissionType = PermissionType.perm_owner
  write: PermissionType = PermissionType.perm_owner
  manage: PermissionType = PermissionType.perm_owner

  # pending_users: Optional[List[EmailStr]] = []
  # pending_groups: Optional[List[int]] = []
  pending_users: Optional[List[Any]] = []
  pending_groups: Optional[List[Any]] = []


  # authorized_users: Optional[List[EmailStr]] = []
  # authorized_groups: Optional[List[int]] = []
  authorized_users: Optional[List[Any]] = []
  authorized_groups: Optional[List[Any]] = []

  ### linked data
  datasets: Any = {}
  # datasets: List[Dataset] = []
  # datasets: List[int] = []

print("=== SCH-schemas_workspace > WorkspaceBase : ", WorkspaceBase)


class WorkspaceCreate(WorkspaceBase):
  pass


class WorkspaceUpdate(WorkspaceBase):
  pass


class Workspace(WorkspaceBase):
  ### meta
  item_type: str = "workspace"
  id: int
  created_date: Optional[datetime.datetime]
  is_active: bool = True

  ### owner
  owner_id: int

  class Config:
    orm_mode = True


class WorkspaceList(Workspace):
  pass
  # owner: User


# class WorkspaceLight(Workspace):
#   ### meta
#   item_type: str = "workspace"
#   id: int
#   created_date: Optional[datetime.datetime]
#   is_active: bool = True

#   ### owner
#   owner_id: int

#   class Config:
#     orm_mode = True

class WorkspacesList(BaseModel):
  __root__: List[Workspace]
