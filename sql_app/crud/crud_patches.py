from . import (pp, Session)

from ..db.database import get_db

from .base import CRUDBase
from ..models.models_patch import Patch
from ..schemas.schemas_patch import PatchCreate, PatchUpdate


class CRUDPatch(CRUDBase[Patch, PatchCreate, PatchUpdate]):
  pass

patch = CRUDPatch(Patch)
