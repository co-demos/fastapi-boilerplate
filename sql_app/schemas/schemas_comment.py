from . import ( List, Optional, BaseModel,
  datetime,
)
from enum import Enum, IntEnum

class CommentType(str, Enum):
  simple_comment = "simple comment"
  important = "important"
  proposal = "proposal"


class CommentStatus(str, Enum):
  new = "new"
  read = "read"
  treated = "treated"
  inappropriate = "inappropriate"


class ToolEnum(IntEnum):
  prio_1 = 1
  prio_2 = 2


class CommentBase(BaseModel):
  body: str


class CommentCreate(CommentBase):
  pass


class CommentUpdate(CommentBase):
  pass


class Comment(CommentBase):
  id: int
  email: str
  created_date: Optional[datetime.datetime]
  post_id: int
  owner_id: int
  comment_type: CommentType = CommentType.simple_comment

  class Config:
    orm_mode = True


class CommentList(Comment):
  pass
