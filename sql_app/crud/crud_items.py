from . import os, Session, datetime, timedelta, Optional

from ..models import models_item
from ..schemas import schemas_item


### ITEM FUNCTIONS

def get_items(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models_item.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas_item.ItemCreate):
# def create_user_item(db: Session, item: schemas_item.ItemCreate, user_id: int):
  # db_item = models_item.Item(**item.dict(), owner_id=user_id)
  db_item = models_item.Item(**item.dict())
  db.add(db_item)
  db.commit()
  db.refresh(db_item)
  return db_item