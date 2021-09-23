from . import (pp, Session)

from ..db.database import get_db

from .base import CRUDBase
from ..models.models_licence import Licence
from ..schemas.schemas_licence import LicenceCreate, LicenceUpdate


class CRUDLicence(CRUDBase[Licence, LicenceCreate, LicenceUpdate]):
  
  def get_by_title(
    self, db: Session,
    title: str,
    user: Optional[User] = None,
    get_auth_check: bool = False,
    req_type: Optional[RequestType] = "read"
    ):
    result = db.query(self.model).filter(self.model.title == title).first()
    if result is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.tablename_singlar} not found")
    
    if get_auth_check :
      check_auth = self.check_user_auth_against_item(db, result, self.tablename_plural, user, req_type)
    
    return result

licence = CRUDLicence(Licence)
