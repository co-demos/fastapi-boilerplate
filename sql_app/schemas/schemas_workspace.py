from . import ( List, Optional, BaseModel,
  datetime
)

from .schemas_dataset import Dataset
from .schemas_permissions import PermissionType

class WorkspaceBase(BaseModel):
  ### basic infos
  title: str
  description: Optional[str] = None

  ### preferences
  color: Optional[str] = None
  icon: Optional[str] = None

  ### access auths
  read: PermissionType = CommentType.perm_owner
  write: PermissionType = CommentType.perm_owner
  manage: PermissionType = CommentType.perm_owner


class WorkspaceCreate(WorkspaceBase):
  pass


class Workspace(WorkspaceBase):
  ### meta
  id: int
  created_date: Optional[datetime.datetime]
  is_active: bool = True

  ### owner
  owner_id: int

  datasets: List[Dataset] = []

  class Config:
    orm_mode = True


class WorkspaceList(Workspace):
  pass
  # owner: User
