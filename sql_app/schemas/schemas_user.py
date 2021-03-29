from . import ( List, Optional, BaseModel,
  EmailStr,
  datetime
)


from .schemas_item import Item
from .schemas_post import Post
from .schemas_comment import Comment


### USER


class UserDelete(BaseModel):
  id: int

class UserBase(BaseModel):
  # email: str
  email: EmailStr
  username: str
  # username: Optional[str] = None


class UserInfos(UserBase):
  name: Optional[str] = None
  surname: Optional[str] = None
  description: Optional[str] = None
  created_date: Optional[datetime.datetime]
  avatar_url: Optional[str] = None


class UserCreate(UserBase):
  password: str


class UserInDBBase(UserInfos):
  id: Optional[int] = None

  class Config:
    orm_mode = True


class User(UserInDBBase):
  is_active: Optional[bool] = None
  is_superuser: bool = False
  items: List[Item] = []
  posts: List[Post] = []
  comments: List[Comment] = []


class UserInDB(User):
  hashed_password: str

