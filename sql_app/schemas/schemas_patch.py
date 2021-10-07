print(">>>>>> import schemas_patch.py >  Patch ...")
from typing import List, Optional, Any
import datetime

from pydantic import BaseModel, EmailStr
# from uuid import UUID

from .schemas_choices import ItemTypeForComments, PatchStatus, PatchStatusAction


class PatchBasics(BaseModel):
  ### basic infos

  ### patch data
  patch_status: PatchStatus = PatchStatus.pending
  patch_to_item_type: ItemTypeForComments = ItemTypeForComments.tabledata
  patch_to_item_id: int

  patch_data: Any = {}

  ### owner (as optional to include not registred users)
  owner_email: Optional[EmailStr]


class PatchGroup(PatchBasics):
  patch_to_item_type: ItemTypeForComments = ItemTypeForComments.group

class PatchWorkspace(PatchBasics):
  patch_to_item_type: ItemTypeForComments = ItemTypeForComments.workspace

class PatchDataset(PatchBasics):
  patch_to_item_type: ItemTypeForComments = ItemTypeForComments.dataset

class PatchTablemeta(PatchBasics):
  patch_to_item_type: ItemTypeForComments = ItemTypeForComments.table

class PatchTabledata(PatchBasics):
  patch_to_item_type: ItemTypeForComments = ItemTypeForComments.tabledata



class PatchCreate(PatchBasics):
  pass


class PatchUpdate(PatchBasics):
  pass


class Patch(PatchBasics):
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


# class PatchList(Patch):
#   pass
#   # owner: User

class PatchesList(BaseModel):
  __root__: List[Patch]
