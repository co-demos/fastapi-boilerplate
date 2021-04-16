from . import (settings, Session, datetime, timedelta,
  Optional,
  HTTPException, status
)

from .base import CRUDBase
from ..models.models_item import Item
from ..schemas.schemas_item import ItemCreate, ItemUpdate


### ITEM FUNCTIONS

class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
  pass

item = CRUDItem(Item)
