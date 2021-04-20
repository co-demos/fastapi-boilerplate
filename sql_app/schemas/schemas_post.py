print(">>>>>> import schemas_post.py >  Post ...")
from typing import List, Optional, Any
import datetime

from pydantic import BaseModel, Field, EmailStr
from uuid import UUID

from .schemas_comment import Comment

class PostBase(BaseModel):
  title: str
  body: Optional[str] = None


class PostCreate(PostBase):
  pass


class PostUpdate(PostBase):
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
