from . import ( List, Session, APIRouter, Depends,
  get_db,
  schemas_post, crud_posts,
  models_user
)

from ..crud.crud_users import (
  get_current_user,
)


router = APIRouter()

@router.post("/", response_model=schemas_post.Post)
def create_post_for_user(
  post: schemas_post.PostCreate, 
  db: Session = Depends(get_db),
  current_user: models_user.User = Depends(get_current_user)
):
  user_id = current_user.id
  return crud_posts.create_user_post(db=db, post=post, user_id=user_id)


@router.get("/{post_id}", response_model=schemas_post.PostList)
def read_post(post_id: int , db: Session = Depends(get_db)):
  post = crud_posts.get_post(db, id=post_id)
  return post


@router.get("/", response_model=List[schemas_post.PostList])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  posts = crud_posts.get_posts(db, skip=skip, limit=limit)
  return posts
