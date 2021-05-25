from . import (pp, Session)

from ..db.database import get_db

from .base import CRUDBase
from ..models.models_group import Group
from ..schemas.schemas_group import GroupCreate, GroupUpdate


class CRUDGroup(CRUDBase[Group, GroupCreate, GroupUpdate]):
  pass

group = CRUDGroup(Group)
