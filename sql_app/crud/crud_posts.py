from . import (settings, Session, datetime, timedelta,
  Optional,
  HTTPException, status
)

from ..models import models_post
from ..schemas import schemas_post


### POSTS FUNCTIONS

def get_post(db: Session, id: int):
  return db.query(models_post.Post).filter(models_post.Post.id == id).first()


def get_posts(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models_post.Post).offset(skip).limit(limit).all()


def create_user_post(db: Session, post: schemas_post.PostCreate, user_id: int):
  db_post = models_post.Post(**post.dict(), owner_id=user_id)
  db.add(db_post)
  db.commit()
  db.refresh(db_post)
  return db_post


def get_user_posts(db: Session, user_id: int):
  return db.query(models_post.Post).filter(models_post.Post.owner_id == user_id).all()
