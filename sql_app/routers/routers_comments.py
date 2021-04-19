from . import ( List, Session, APIRouter, Depends,
  HTTPException, status,
  get_db,
  # schemas_comment,
  crud_comments,
  # models_user
)

from ..crud.crud_users import (
  get_current_user,
)

from ..models.models_user import User
from ..schemas.schemas_comment import CommentList


router = APIRouter()


@router.get(
  "/{comment_id}",
  summary="Get an comment",
  description="Get an comment given its id",
  response_model=CommentList
)
def read_comment(
  comment_id: int,
  db: Session = Depends(get_db)
  ):
  comment = crud_comments.get_comment(db, id=comment_id)
  if comment is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
  return comment


@router.get(
  "/",
  summary="Get a list of comments",
  description="Get a list of all comments given a limit",
  response_model=List[CommentList]
)
def read_comments(
  skip: int = 0, limit: int = 100,
  db: Session = Depends(get_db)
  ):
  comments = crud_comments.get_comments(db, skip=skip, limit=limit)
  return comments
