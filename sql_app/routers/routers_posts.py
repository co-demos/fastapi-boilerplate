from . import ( List, Query,
  Session, APIRouter, Depends,
  HTTPException, status,
  get_db,
  schemas_post, crud_posts,
  schemas_comment, crud_comments,
  models_user
)

from ..crud.crud_users import (
  get_current_user,
)


router = APIRouter()


@router.post(
  "/",
  summary="Create an post",
  description="Create an postt, including the id of the user creating the post",
  response_model=schemas_post.Post, status_code=status.HTTP_201_CREATED
)
def create_post_for_user(
  post: schemas_post.PostCreate, 
  db: Session = Depends(get_db),
  current_user: models_user.User = Depends(get_current_user)
  ):
  user_id = current_user.id
  return crud_posts.create_user_post(db=db, post=post, user_id=user_id)


@router.get(
  "/{post_id}",
  summary="Get an post",
  description="Get an post by its id",
  response_model=schemas_post.PostList
)
def read_post(
  post_id: int ,
  db: Session = Depends(get_db)
  ):
  post = crud_posts.get_post(db, id=post_id)
  if post is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
  return post


@router.post(
  "/{post_id}/comment",
  summary="Create an comment on a post",
  description="Create an comment associated to a post and an user",
  response_model=schemas_comment.Comment, status_code=status.HTTP_201_CREATED
)
def create_comment_for_user_and_post(
  post_id: int,
  comment: schemas_comment.CommentCreate, 
  comment_type: schemas_comment.CommentType = schemas_comment.CommentType.proposal,
  db: Session = Depends(get_db),
  current_user: models_user.User = Depends(get_current_user)
  ):
  user_id = current_user.id
  user_email = current_user.email
  return crud_comments.create_user_comment_on_post(
    db=db,
    comment=comment,
    comment_type=comment_type,
    user_id=user_id,
    user_email=user_email,
    post_id=post_id
  )


@router.get(
  "/",
  summary="Get a list of posts",
  description="Get a list of all posts given a limit",
  response_model=List[schemas_post.PostList]
)
def read_posts(
  skip: int = 0, limit: int = 100,
  db: Session = Depends(get_db)
  ):
  posts = crud_posts.get_posts(db, skip=skip, limit=limit)
  return posts
