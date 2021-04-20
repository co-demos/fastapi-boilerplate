print(">>>>>> import schemas_item.py >  Item ...")
from typing import List, Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
  title: str
  description: Optional[str] = None


class ItemCreate(ItemBase):
  pass


class ItemUpdate(ItemBase):
  pass


class Item(ItemBase):
  id: int
  owner_id: int

  class Config:
    orm_mode = True


class ItemList(Item):
  # owner: User
  pass
