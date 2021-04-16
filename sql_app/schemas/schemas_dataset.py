from . import ( List, Optional, BaseModel,
  datetime
)

# from .schemas_Table import Table
from .schemas_permissions import PermissionType

class DatasetBase(BaseModel):
  ### basic infos
  title: str
  description: Optional[str] = None
  licence: str

  ### preferences
  color: Optional[str] = None
  icon: Optional[str] = None

  ### access auths
  read: PermissionType = CommentType.perm_owner
  comment: PermissionType = CommentType.perm_owner
  patch: PermissionType = CommentType.perm_owner
  write: PermissionType = CommentType.perm_owner
  manage: PermissionType = CommentType.perm_owner


class DatasetCreate(DatasetBase):
  pass


class Dataset(DatasetBase):
  ### meta
  id: int
  created_date: Optional[datetime.datetime]
  is_active: bool = True

  ### owner
  owner_id: int

  # datasets: List[Dataset] = []

  class Config:
    orm_mode = True


class DatasetList(Dataset):
  pass
  # owner: User
