print(">>>>>> import schemas_licence.py >  Licence ...")
from typing import Optional
import datetime

from pydantic import BaseModel

class LicenceBase(BaseModel):
  ### basic infos
  title: str
  fullname: str
  category: Optional[str] = None
  url: Optional[str] = None


class LicenceCreate(LicenceBase):
  pass


class LicenceUpdate(LicenceBase):
  pass


class Licence(LicenceBase):
  ### meta
  item_type: str = "licence"
  id: int
  created_date: Optional[datetime.datetime]
  is_active: bool = True

  class Config:
    orm_mode = True


class LicenceList(Licence):
  pass


class LicencesList(BaseModel):
  __root__: List[Licence] = []
