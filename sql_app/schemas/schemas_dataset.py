print(">>>>>> import schemas_dataset.py >  Dataset ...")
from typing import List, Optional
import datetime

from pydantic import BaseModel

from .schemas_permissions import PermissionType
# from .schemas_workspace import Workspace
# from .schemas_Table import Table

class DatasetBase(BaseModel):
  ### basic infos
  title: str = "My dataset title"
  description: Optional[str] = "My dataset description"
  licence: str

  ### preferences
  color: Optional[str] = "black"
  icon: Optional[str] = "icon-table"

  ### access auths
  read: PermissionType = PermissionType.perm_owner
  comment: PermissionType = PermissionType.perm_owner
  patch: PermissionType = PermissionType.perm_owner
  write: PermissionType = PermissionType.perm_owner
  manage: PermissionType = PermissionType.perm_owner


class DatasetCreate(DatasetBase):
  # from_workspace_id: Optional[int]
  pass


class DatasetUpdate(DatasetBase):
  pass


class Dataset(DatasetBase):
  ### meta
  id: int
  created_date: Optional[datetime.datetime]
  is_active: bool = True

  ### owner
  owner_id: int

  ### linked data
  # workspace_related: List[Workspace] = []
  # tables: List[Table] = []

  class Config:
    orm_mode = True


class DatasetList(Dataset):
  pass
  # owner: User
