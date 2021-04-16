from . import ( List, Optional, BaseModel,
  datetime
)

class LicenceBase(BaseModel):
  ### basic infos
  title: str
  fullname: str
  category: Optional[str] = None
  url: Optional[str] = None


class LicenceCreate(LicenceBase):
  pass


class Licence(LicenceBase):
  ### meta
  id: int
  created_date: Optional[datetime.datetime]
  is_active: bool = True

  class Config:
    orm_mode = True


class LicenceList(Licence):
  pass
