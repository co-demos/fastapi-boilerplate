from . import (pp, Session)

from typing import Any, Optional

from ..db.database import get_db

from .base import CRUDBase

from ..models.models_user import User

from ..models.models_comment import Comment
from ..schemas.schemas_comment import CommentCreate, CommentUpdate

from ..schemas.schemas_choices import RequestType


class CRUDComment(CRUDBase[Comment, CommentCreate, CommentUpdate]):
  
  # def get_by_id(
  #   self, db: Session, 
  #   id: Any,
  #   user: Optional[User] = None,
  #   get_auth_check: bool = True,
  #   req_type: Optional[RequestType] = "read"
  #   ) :

  #   print("\nget_by_id > self.model.__tablename__ :", self.model.__tablename__)
  #   print("get_by_id > self.model.__dict__ :", self.model.__dict__)
    
  #   result = db.query(self.model).filter(self.model.id == id).first()
  #   print("\nget_by_id > result :", result)

  #   related_item_id = result.comment_to_item_id
  #   comment_to_item_type = result.comment_to_item_type
  #   print("get_by_id > related_item_id :", related_item_id)
  #   print("get_by_id > comment_to_item_type :", comment_to_item_type)

  #   if result is None:
  #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.tablename_singlar} not found")
    
  #   if get_auth_check :
  #     check_auth = self.check_user_auth_against_item(db, result, self.tablename_plural, user, req_type)
    
  #   return result

  pass 

comment = CRUDComment(Comment)
