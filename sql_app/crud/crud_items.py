from . import (os, Session, datetime, timedelta,
  Optional,
  HTTPException, status
)

from ..models import models_item
from ..schemas import schemas_item


### ITEM FUNCTIONS

def get_item(db: Session, id: int):
  return db.query(models_item.Item).filter(models_item.Item.id == id).first()


def get_items(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models_item.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas_item.ItemCreate, user_id: int):
  db_item = models_item.Item(**item.dict(), owner_id=user_id)
  db.add(db_item)
  db.commit()
  db.refresh(db_item)
  return db_item


def get_user_items(db: Session, user_id: int):
  return db.query(models_item.Item).filter(models_item.Item.owner_id == user_id).all()
