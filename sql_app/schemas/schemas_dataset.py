print(">>>>>> import schemas_dataset.py >  Dataset ...")
from typing import List, Optional
import datetime

from pydantic import BaseModel

from .schemas_permissions import PermissionType
# from .schemas_workspace import Workspace
from .schemas_tablemeta import Tablemeta, TablemetaCreate

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


class DatasetData(DatasetBase): 
  tables: Optional[List[Tablemeta]] = []


class DatasetCreate(DatasetData):
  tables: Optional[List[TablemetaCreate]] = []


class DatasetUpdate(DatasetData):
  pass


class Dataset(DatasetData):
  ### meta
  id: int
  created_date: Optional[datetime.datetime]
  is_active: bool = True

  ### owner
  owner_id: int

  ### linked data
  # workspace_related: List[Workspace] = []

  class Config:
    orm_mode = True


class DatasetList(Dataset):
  pass
  # owner: User