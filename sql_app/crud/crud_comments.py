from . import (os, Session, datetime, timedelta,
  Optional,
  HTTPException, status
)

from ..models import models_comment
from ..schemas import schemas_comment


### COMMENTS FUNCTIONS

def get_comment(db: Session, id: int):
  return db.query(models_comment.Comment).filter(models_comment.Comment.id == id).first()


def get_comments(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models_comment.Comment).offset(skip).limit(limit).all()


def create_user_comment_on_post(db: Session, comment: schemas_comment.CommentCreate, user_id: int, post_id: id):
  db_comment = models_comment.Comment(**comment.dict(), owner_id=user_id, post_id=post_id)
  db.add(db_comment)
  db.commit()
  db.refresh(db_comment)
  return db_comment


def get_user_comments(db: Session, user_id: int):
  return db.query(models_comment.Comment).filter(models_comment.Comment.owner_id == user_id).all()


def get_post_comments(db: Session, post_id: int):
  return db.query(models_comment.Comment).filter(models_comment.Comment.post_id == post_id).all()
