from sqlalchemy.orm import Session

from ..crud import crud_users, crud_licences
from ..schemas import schemas_user, schemas_licence
from ..core.config import settings
from ..core.licences import main_licences
from ..db import *  # noqa: F401

# make sure all SQL Alchemy models are imported (..db) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    ### add superuser from .env file
    user_in_db = crud_users.get_user_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user_in_db:
      user_in = schemas_user.UserCreate(
        email=settings.FIRST_SUPERUSER,
        username=settings.FIRST_SUPERUSER_USERNAME,
        name=settings.FIRST_SUPERUSER_NAME,
        surname=settings.FIRST_SUPERUSER_SURNAME,
        locale=settings.FIRST_SUPERUSER_LOCALE,
        description=settings.FIRST_SUPERUSER_DESCRIPTION,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        is_active=True,
        is_superuser=True,
      )
      print (">>> init_db.py > init_db > user_in :", user_in)
      user_in_db = crud_users.create_user_in_db(db, user=user_in)  # noqa: F841
    
    ### add licences
    print (">>> init_db.py > init_db > main_licences :", main_licences)
    for licence in main_licences: 
      licence_in_db = crud_licences.get_licence_by_title(db, title=licence["title"])
      print (">>> init_db.py > init_db > licence_in_db :", licence_in_db.__dict__)
      if not licence_in_db:
        licence_in = schemas_licence.LicenceCreate(
          title=licence["title"],
          fullname=licence["fullname"],
          category=licence["category"],
          url=licence["url"],
        )
        print (">>> init_db.py > init_db > licence_in :", licence_in)
        licence_in_db = crud_licences.create_licence_in_db(db, licence=licence_in)  # noqa: F841

