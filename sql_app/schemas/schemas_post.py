from . import ( List, Optional, BaseModel,
  datetime
)

from .schemas_comment import Comment

class PostBase(BaseModel):
  title: str
  body: Optional[str] = None


class PostCreate(PostBase):
  pass


class Post(PostBase):
  id: int
  created_date: Optional[datetime.datetime]
  owner_id: int
  post_comments: List[Comment] = []

  class Config:
    orm_mode = True


class PostList(Post):
  pass
  # owner: User
