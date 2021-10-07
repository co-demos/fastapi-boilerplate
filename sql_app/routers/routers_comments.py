print(">>>>>> import routers.routers_comments.py ...")

from . import ( List, Session, APIRouter, Depends,
  HTTPException, status, BackgroundTasks,
  get_db, Query
)

from ..schemas.schemas_comment import Comment, CommentCreate, CommentUpdate, CommentsList
from ..crud.crud_comments import comment

from ..models.models_user import User

from ..crud.crud_users import (
  get_current_user,
  get_current_user_optional,
  get_current_active_user,
)

from ..models.models_user import User
# from ..schemas.schemas_comment import CommentList


router = APIRouter()


@router.post("/",
  summary="Create a comment",
  description="Create a comment, including the email of the user creating the comment - authentication is optional",
  response_model=Comment,
  status_code=status.HTTP_201_CREATED
  )
def create_comment(
  obj_in: CommentCreate,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user_optional)
  ):
  ### TO DO 
  ### must check if target item allows comments
  return comment.create(db=db, obj_in=obj_in)


@router.get("/{comment_id}",
  summary="Get a comment",
  description="Get a comment given its id - authentication is optional",
  response_model=Comment
)
def read_comment(
  obj_id: int, 
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user_optional)
  ):
  comment_in_db = workspace.get_by_id(db, id=obj_id, user=current_user, req_type="read")
  return comment_in_db


@router.delete("/{obj_id}",
  summary="Delete a comment",
  description="Delete a comment by its id",
  response_model=Comment
  )
def delete_comment(
  obj_id: int,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  print("delete_comment > obj_id : ", obj_id)
  comment_deleted = comment.remove(db=db, id=obj_id, current_user=current_user)
  print("delete_comment > comment_deleted : ", comment_deleted)
  return comment_deleted
