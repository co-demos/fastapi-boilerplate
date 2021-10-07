from . import (pp, Session)

from ..db.database import get_db

from .base import CRUDBase
from ..models.models_comment import Comment
from ..schemas.schemas_comment import CommentCreate, CommentUpdate


class CRUDComment(CRUDBase[Comment, CommentCreate, CommentUpdate]):
  pass

comment = CRUDComment(Comment)
