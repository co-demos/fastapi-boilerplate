from . import (pp, Session)

from ..db.database import get_db

from ..models import models_licence
from ..schemas import schemas_licence


###  LICENCE FUNCTIONS

def get_licence_by_id(db: Session, licence_id: int):
  return db.query(models_licence.Licence).get(licence_id)


def get_licence_by_title(db: Session, title: str):
  return db.query(models_licence.Licence).filter(models_licence.Licence.title == title).first()


def update_licence_field_in_db(
  db: Session,
  licence_id: int,
  field: str,
  value: any
  ):
  # print("update_licence_field_in_db > field : ", field)
  # print("update_licence_field_in_db > value : ", value)
  db_licence = get_licence_by_id(db=db, licence_id=licence_id)
  # print("update_licence_field_in_db > db_licence : ", db_licence)
  setattr(db_licence, field, value)
  db.add(db_licence)
  db.commit()
  db.refresh(db_licence)
  return db_licence


def delete_licence_in_db(
  db: Session,
  licence_id: int, 
  ):

  obj = db.query(models_licence.Licence).get(licence_id)
  print("delete_licence_in_db > obj :")
  if not obj:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Licence not found"
    )
  # pp.pprint(obj.__dict__)
  db.delete(obj)
  db.commit()
  return obj


def create_licence_in_db(db: Session, licence: schemas_licence.LicenceCreate):
  print("create_licence_in_db > licence : ", licence)
  db_licence = models_licence.Licence(
    title=licence.title,
    fullname=licence.fullname,
    category=licence.category,
    url=licence.url,
  )
  print("create_licence_in_db > db_licence : ", db_licence)
  db.add(db_licence)
  db.commit()
  db.refresh(db_licence)
  return db_licence



### LICENCES FUNCTIONS

def get_licences(db: Session):
  return db.query(models_licence.Licence).all()

