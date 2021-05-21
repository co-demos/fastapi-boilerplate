print(">>>>>> import schemas_tablemeta.py >  Table ...")
from typing import List, Dict, Optional, Any
import datetime

from pydantic import BaseModel
from enum import Enum

from .schemas_permissions import PermissionType

# from .schemas_workspace import Workspace
# from .schemas_dataset import Dataset

from .schemas_field_data import FieldData


### SCHEMAS - TABLE META

class TablemetaBase(BaseModel):
  ### basic infos
  title: str = "My table title"
  description: Optional[str] = "My table description"
  licence: str
  dataset_id: Optional[int] = None # parent dataset

  ### preferences
  # color: Optional[str] = "black"
  # icon: Optional[str] = "icon-table"

  ### access auths
  read: PermissionType = PermissionType.perm_owner
  comment: PermissionType = PermissionType.perm_owner
  patch: PermissionType = PermissionType.perm_owner
  write: PermissionType = PermissionType.perm_owner
  manage: PermissionType = PermissionType.perm_owner

  ### table data
  table_fields : List[FieldData] = []


class TablemetaCreate(TablemetaBase):
  ### table data at creation
  table_data : Any = [] ### receive raw data


class TablemetaData(TablemetaBase):
  table_data_uuid : str = None ### send only table_data's table identifier


class TablemetaUpdate(TablemetaData):
  pass


class Tablemeta(TablemetaData):
  ### meta
  item_type: str = "table"
  id: int
  created_date: Optional[datetime.datetime]
  is_active: bool = True
  
  dataset_id: int # parent dataset

  ### owner
  owner_id: int

  ### linked data
  dataset_id: int = None # parent dataset

  class Config:
    orm_mode = True


class TablemetaList(Tablemeta):
  pass
  # owner: User


### SCHEMAS - TABLE DATA

class UpdateType(str, Enum):
  cell = "cell"
  row = "row"
  rows = "rows"


class TabledataCell(BaseModel):
  row_id: int
  column: str
  value: Any


class TabledataUpdate(BaseModel):
  item_type: str = "table_data"
  update_type: UpdateType = UpdateType.cell
  tablemeta_id: int
  table_data_uuid: str


class TabledataUpdateCell(TabledataUpdate):
  table_data_cell: TabledataCell


class TabledataUpdateRow(TabledataUpdate):
  table_data_row_id: int
  table_data_row: Any = {}


class TabledataAddRow(TabledataUpdate):
  table_data_row: Any = {}


class TabledataDeleteRow(TabledataUpdate):
  update_type: UpdateType = UpdateType.row
  table_data_row_id: int
  

class TabledataUpdateRows(TabledataUpdate):
  table_data_rows: Any = []
