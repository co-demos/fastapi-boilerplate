print(">>>>>> import schemas_sockets.py >  Sockets ...")
from typing import List, Optional, Any, Union
import datetime

from pydantic import BaseModel, EmailStr
# from uuid import UUID

from .schemas_choices import ItemTypeExtended, InvitationStatusAction, EmitAction
# from .schemas_auths import AuthsInfosBasics


class SocketBase(BaseModel):
  sid: str


class CreateOwnRoom(SocketBase):
  user_email: Optional[EmailStr]
  user_id: Optional[int]


class BroadcastAction(BaseModel):

  from_user_username: Optional[str]
  from_user_name: Optional[str]
  from_user_surname: Optional[str]
  from_user_username: Optional[str]
  from_user_email: EmailStr
  # from_user_id: Optional[int]

  target_rooms: List[EmailStr]

  item_type: ItemTypeExtended
  item_id: int

  action: EmitAction

