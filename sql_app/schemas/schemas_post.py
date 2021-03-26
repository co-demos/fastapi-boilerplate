from . import ( List, Optional, BaseModel,
  datetime
)

# from .schemas_user import User

class PostBase(BaseModel):
  title: str
  body: Optional[str] = None


class PostCreate(PostBase):
  pass


class Post(PostBase):
  id: int
  created_date: Optional[datetime.datetime]
  owner_id: int

  class Config:
    orm_mode = True


class PostList(Post):
  pass
  # owner: User
