from . import (pp, Session)
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from sqlalchemy import and_, or_, not_, func, tuple_, text, cast

from ..db.database import get_db

from .base import CRUDBase
from ..models.models_user import User
from ..models.models_invitation import Invitation
from ..schemas.schemas_invitation import InvitationCreate, InvitationUpdate
from ..schemas.schemas_choices import InvitationStatusAction


class CRUDInvitation(CRUDBase[Invitation, InvitationCreate, InvitationUpdate]):
  def get_multi_received(
    self, db: Session, *,
    user: User,
    skip: int = 0,
    limit: int = 100,
    ) -> List[Invitation]:

    ### filter out invitations owner sent him.her.self
    items_in_db = db.query(self.model).filter(
      and_(
        self.model.invitee == user.email,
        self.model.owner_id != user.id,
      )
    )

    if skip > 0 :
      items_in_db = items_in_db.offset(skip)
    if limit and limit > 0 :
      items_in_db = items_in_db.limit(limit)

    return items_in_db.all()


  def update_status(
    self, db: Session, *,
    db_obj: Invitation,
    status: InvitationStatusAction
    ):
    setattr(db_obj, 'invitation_status', status)
    print("update > db_obj : ", db_obj)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


invitation = CRUDInvitation(Invitation)


