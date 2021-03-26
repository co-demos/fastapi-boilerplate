from . import ( List, Optional, BaseModel,
  datetime
)

# from .schemas_user import User

class CommentBase(BaseModel):
  email:str
  body: Optional[str] = None


class CommentCreate(CommentBase):
  pass
  # owner_id: int


class Comment(CommentBase):
  id: int
  created_date: Optional[datetime.datetime]
  post_id: int
  owner_id: int

  class Config:
    orm_mode = True


class CommentList(Comment):
  pass
  # owner: User
