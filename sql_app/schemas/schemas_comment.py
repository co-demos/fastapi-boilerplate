print(">>>>>> import schemas_comment.py >  Comment ...")
from typing import List, Optional
import datetime

from pydantic import BaseModel, EmailStr
from enum import Enum, IntEnum


from .schemas_choices import ItemTypeForComments

from .schemas_patch import Patch, PatchCreate
# from .schemas_user import User, UserInDBBaseLight



class CommentStatus(str, Enum):
  new = "new"
  read = "read"
  treated = "treated"
  inappropriate = "inappropriate"


class CommentBasics(BaseModel):
  
  ### basic infos
  # title: Optional[str]
  message: str

  ### related data
  comment_to_item_id: int
  comment_to_item_type: ItemTypeForComments = ItemTypeForComments.comment
  comment_status: CommentStatus = CommentStatus.new
  response_to_comment_id: Optional[int]

  ### patch data  (optional)
  patch: Optional[Patch]
  patch_data: Optional[PatchCreate]

  ### owner (as optional to include not registred users)
  owner_email: Optional[EmailStr]
  alert_item_owner: Optional[bool] = False


class CommentComment(CommentBasics):
  comment_to_item_type: ItemTypeForComments = ItemTypeForComments.comment

class CommentUser(CommentBasics):
  comment_to_item_type: ItemTypeForComments = ItemTypeForComments.user

class CommentGroup(CommentBasics):
  comment_to_item_type: ItemTypeForComments = ItemTypeForComments.group

class CommentInvitation(CommentBasics):
  comment_to_item_type: ItemTypeForComments = ItemTypeForComments.invitation

class CommentWorkspace(CommentBasics):
  comment_to_item_type: ItemTypeForComments = ItemTypeForComments.workspace

class CommentDataset(CommentBasics):
  comment_to_item_type: ItemTypeForComments = ItemTypeForComments.dataset

class CommentTablemeta(CommentBasics):
  comment_to_item_type: ItemTypeForComments = ItemTypeForComments.table

class CommentTabledata(CommentBasics):
  comment_to_item_type: ItemTypeForComments = ItemTypeForComments.tabledata


class CommentCreate(CommentBasics):
  comment_status = CommentStatus.new
  patch_data: Optional[PatchCreate]


class CommentUpdate(BaseModel):
  id: int
  comment_status: CommentStatus = CommentStatus.new


class Comment(CommentBasics):
  ### meta
  item_type: str = "comment"
  id: int
  created_date: Optional[datetime.datetime]
  is_active: bool = True

  # has_patch: bool = False
  patch_id: Optional[int]

  class Config:
    orm_mode = True


class CommentsList(BaseModel):
  __root__: List[Comment]
