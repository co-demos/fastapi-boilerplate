from . import ( List, Optional, BaseModel,
  datetime
)

# from .schemas_user import User

class CommentBase(BaseModel):
  body: str


class CommentCreate(CommentBase):
  pass


class Comment(CommentBase):
  id: int
  email: str
  created_date: Optional[datetime.datetime]
  post_id: int
  owner_id: int

  class Config:
    orm_mode = True


class CommentList(Comment):
  pass
  # owner: User
