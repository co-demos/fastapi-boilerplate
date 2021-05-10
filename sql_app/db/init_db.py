from sqlalchemy.orm import Session

# from ..crud import crud_users
from ..crud.crud_users import user
from ..crud.crud_licences import licence

from ..schemas import schemas_user
from ..schemas.schemas_licence import LicenceCreate, LicenceUpdate

from ..core.config import settings
from ..core.licences import main_licences

# from .base_class import BaseCommons
# from ..models import (
  
#   models_item, 
#   models_post,
#   models_comment,

#   models_licence,
#   models_tablemeta,
#   models_dataset,
#   models_workspace,
#   models_user,
# )

from ..db import *  # noqa: F401

# make sure all SQL Alchemy models are imported (..db) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine_commons)

    ### add superuser from .env file
    # user_in_db = crud_users.get_user_by_email(db, email=settings.FIRST_SUPERUSER)
    user_in_db = user.get_user_by_email(db=db, email=settings.FIRST_SUPERUSER)
    if not user_in_db:
      user_in = schemas_user.UserSuper(
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
      # user_in_db = crud_users.create_user_in_db(db, user=user_in, superuser=True)  # noqa: F841
      user_in_db = user.create_user_in_db(db=db, user_in=user_in, superuser=True)  # noqa: F841
    
    ### add licences
    # print (">>> init_db.py > init_db > main_licences :", main_licences)
    for licence_raw in main_licences: 
      # print (">>> init_db.py > init_db > licence_raw['title'] :", licence_raw['title'])
      licence_in_db = licence.get_by_title(db, title=licence_raw['title'])
      # print (">>> init_db.py > init_db > licence_in_db :", licence_in_db.__dict__)
      if not licence_in_db:
        licence_in = LicenceCreate(
          title=licence_raw["title"],
          fullname=licence_raw["fullname"],
          category=licence_raw["category"],
          url=licence_raw["url"],
        )
        # print (">>> init_db.py > init_db > licence_in :", licence_in)
        licence_in_db = licence.create(db=db, obj_in=licence_in)  # noqa: F841

