from . import (settings, Session, datetime, timedelta,
  Optional,
  HTTPException, status
)

from ..models.models_post import Post
from ..schemas.schemas_post import PostCreate


### POSTS FUNCTIONS

def get_post(db: Session, id: int):
  return db.query(Post).filter(Post.id == id).first()


def get_posts(db: Session, skip: int = 0, limit: int = 100):
  return db.query(Post).offset(skip).limit(limit).all()


def create_user_post(db: Session, post: PostCreate, user_id: int):
  db_post = Post(**post.dict(), owner_id=user_id)
  db.add(db_post)
  db.commit()
  db.refresh(db_post)
  return db_post


def get_user_posts(db: Session, user_id: int):
  return db.query(Post).filter(Post.owner_id == user_id).all()
