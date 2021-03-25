from . import ( List, Optional, BaseModel,
  datetime
)

# from .schemas_user import User

class PostBase(BaseModel):
  title: str
  body: Optional[str] = None


class PostCreate(PostBase):
  pass
  # owner_id: int


class Post(PostBase):
  id: int
  created_date: Optional[datetime.datetime]

  class Config:
    orm_mode = True


class PostList(Post):
  owner_id: int
  # owner: User
