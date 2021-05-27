from . import (pp, Session)

from ..db.database import get_db

from .base import CRUDBase
from ..models.models_invitation import Invitation
from ..schemas.schemas_invitation import InvitationCreate, InvitationUpdate


class CRUDInvitation(CRUDBase[Invitation, InvitationCreate, InvitationUpdate]):
  pass

invitation = CRUDInvitation(Invitation)


