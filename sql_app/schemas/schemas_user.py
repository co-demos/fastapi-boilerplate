from . import ( List, Optional, BaseModel,
  EmailStr,
  datetime
)

from .schemas_workspace import Workspace
from .schemas_dataset import Dataset

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
  name: Optional[str] = "Elinor"
  surname: Optional[str] = "Ostrom"
  locale: Optional[str] = "en"
  description: Optional[str] = "User description"

  ### preferences
  avatar_url: Optional[str] = None


class UserInfos(UserBase, UserBasicInfos):
  ### meta
  created_date: Optional[datetime.datetime]


class UserCreate(UserBase, UserBasicInfos):
  ### secret
  password: str


class UserUpdate(UserBase, UserBasicInfos):
  pass


class UserInDBBase(UserInfos):
  ### meta
  id: Optional[int] = None

  class Config:
    orm_mode = True


class User(UserInDBBase):
  ### meta
  is_active: Optional[bool] = None

  ### access auths
  is_superuser: bool = False

  ### linked data
  items: List[Item] = []
  posts: List[Post] = []
  comments: List[Comment] = []

  my_workspaces: List[Workspace] = []
  my_datasets: List[Dataset] = []
  # my_tables: List[Table] = []
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


class UserSuper(UserInDBBase, UserCreate):
  pass

class UserInDB(User):
  ### secret
  hashed_password: str


class UserList(User):
  pass
