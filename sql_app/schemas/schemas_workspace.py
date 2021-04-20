print(">>>>>> import schemas_workspace.py >  Workspace ...")
from typing import List, Optional, Any
import datetime

from pydantic import BaseModel
# from uuid import UUID

from .schemas_dataset import Dataset
from .schemas_permissions import PermissionType


class WorkspaceBase(BaseModel):
  ### basic infos
  title: str = "My workspace"
  description: Optional[str] = "My workspace description"

  ### preferences
  color: Optional[str] = "black"
  icon: Optional[str] = "icon-database"

  ### access auths
  read: PermissionType = PermissionType.perm_owner
  write: PermissionType = PermissionType.perm_owner
  manage: PermissionType = PermissionType.perm_owner

  ### linked data
  datasets: Any = {}
  # datasets: List[Dataset] = []
  # datasets: List[int] = []


class WorkspaceCreate(WorkspaceBase):
  pass


class WorkspaceUpdate(WorkspaceBase):
  pass


class Workspace(WorkspaceBase):
  ### meta
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
