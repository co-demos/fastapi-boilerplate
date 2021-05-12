print(">>>>>> import schemas_user.py >  User ...")
from typing import List, Optional, Any
import datetime

from pydantic import BaseModel, EmailStr
# from uuid import UUID

from .schemas_workspace import Workspace
from .schemas_dataset import Dataset
from .schemas_tablemeta import Tablemeta

from .schemas_item import Item
from .schemas_post import Post
from .schemas_comment import Comment


### USER

class UserDelete(BaseModel):
  id: int


class UserBase(BaseModel):
  ### basic infos - mandatory
  # email: str
  email: EmailStr
  username: str = "Eli"
  # username: Optional[str] = None


class UserBasicInfos(BaseModel):
  ### basic infos
  username: str = "Eli"
  name: Optional[str] = "Elinor"
  surname: Optional[str] = "Ostrom"
  locale: Optional[str] = "en"
  description: Optional[str] = "User description"


class UserBasicInfosAvatar(BaseModel):
  ### preferences
  avatar_url: Optional[str] = None


class UserInfos(UserBase, UserBasicInfos, UserBasicInfosAvatar):
  ### meta
  created_date: Optional[datetime.datetime]
  modif_date: Optional[datetime.datetime]


class UserCreate(UserBase, UserBasicInfos, UserBasicInfosAvatar):
  ### secret
  password: str


class UserUX(BaseModel):
  ### UX
  ux_app: Any = {}
  ux_workspaces: Any = {}
  ux_datasets: Any = {}


class UserInDBBase(UserInfos, UserUX):
  ### meta
  id: Optional[int] = None

  ### linked data
  items: List[Item] = []
  posts: List[Post] = []
  comments: List[Comment] = []

  my_workspaces: List[Workspace] = []
  my_datasets: List[Dataset] = []
  # my_tables: List[Tablemeta] = []
  # my_schemas: List[Schema] = []
  # my_fields: List[Field] = []
  # my_groups: List[Group] = []
  # my_invitations: List[Invitation] = []
  # my_notification: List[Notifications] = []

  # shared_workspaces: List[Workspace] = []
  # shared_datasets: List[Dataset] = []
  # shared_tables: List[Table] = []
  # shared_schemas: List[Schema] = []
  # shared_fields: List[Field] = []

  class Config:
    orm_mode = True


class User(UserInDBBase):
  ### meta
  item_type: str = "user"
  is_active: Optional[bool] = None

  ### access auths
  is_superuser: bool = False


class UserUpdate(UserInDBBase):
  pass


class UserSuper(UserInDBBase, UserCreate):
  pass


class UserInDB(User):
  ### secret
  hashed_password: str


class UserList(User):
  pass
