print(">>>>>> import schemas_field_data.py > FieldData ...")
from typing import List, Optional, Any, Union

from enum import Enum
import datetime

from pydantic import BaseModel

from .schemas_permissions import PermissionType

# cf : https://schema.data.gouv.fr/schemas/etalab/schema-inclusion-numerique/0.1.1/schema.json

class FieldType(str, Enum):
  str_ = "str"
  longStr_ = "longStr"
  int_ = "int"
  float_ = "float"
  bool_ = "bool"
  date_ = "date"
  tag_ = "tag"
  rating_ = "rating"
  url_ = "url"
  email_ = "email"
  latlon_ = "latlon"
  json_ = "json"
  html_ = "html"
  md_ = "md"
  curr_ = "curr"
  ref_ = "ref"
  refs_ = "refs"
  color_ = "color"


class FieldDataBase(BaseModel):
  
  ### basic infos
  value: str = "My field value"  # aka name
  text: str = "fieldValue" # aka name full
  field_type : FieldType = FieldType.str_
  field_code : Optional[str]

  description: Optional[str] = "My field description"
  example: Optional[str] = "An example"

  # options for display or validation / ex: enumeration values, range, etc... 
  constraints: Optional[Any] = { 
    'required' : False 
  }

  ### access auths
  read: PermissionType = PermissionType.perm_owner
  # comment: PermissionType = PermissionType.perm_owner
  # patch: PermissionType = PermissionType.perm_owner
  write: PermissionType = PermissionType.perm_owner
  manage: PermissionType = PermissionType.perm_owner

  ### ux infos
  width: Union[int, str] = "auto"
  hide: Optional[bool] = False
  fixed: Optional[bool] = False

  class Config:  
    use_enum_values = True


class FieldDataCreate(FieldDataBase):
  # from_workspace_id: Optional[int]
  pass


class FieldDataUpdate(FieldDataBase):
  pass


class FieldData(FieldDataBase):
  ### meta
  item_type: str = "field"
  id: int
  created_date: Optional[datetime.datetime]
  is_active: bool = True

  ### owner
  owner_id: int

class FieldDataList(FieldData):
  pass
  # owner: User
