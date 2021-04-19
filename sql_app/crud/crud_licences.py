from . import (pp, Session)

from ..db.database import get_db

from .base import CRUDBase
from ..models.models_licence import Licence
from ..schemas.schemas_licence import LicenceCreate, LicenceUpdate


class CRUDLicence(CRUDBase[Licence, LicenceCreate, LicenceUpdate]):
  pass

licence = CRUDLicence(Licence)
