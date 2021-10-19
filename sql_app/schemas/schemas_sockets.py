print(">>>>>> import schemas_sockets.py >  Sockets ...")
from typing import List, Optional, Any, Union
import datetime

from pydantic import BaseModel, EmailStr
# from uuid import UUID

from .schemas_choices import ( 
  ItemTypeExtended, InvitationStatusAction, 
  EmitAction, CallbackMethod
)
# from .schemas_auths import AuthsInfosBasics


class SocketBase(BaseModel):
  sid: str


class CreateOwnRoom(SocketBase):
  user_email: Optional[EmailStr]
  user_id: Optional[int]


class CreateItemRoom(SocketBase):
  item_type: ItemTypeExtended
  item_id: int


class Callback(BaseModel):
  method: CallbackMethod
  url: Optional[str]
  item_type: ItemTypeExtended
  get_list: bool = False


class BroadcastAction(BaseModel):

  from_user_username: Optional[str]
  from_user_name: Optional[str]
  from_user_surname: Optional[str]
  from_user_username: Optional[str]
  from_user_email: EmailStr
  # from_user_id: Optional[int]

  target_rooms: List[EmailStr]
  include_sid: Optional[bool] = False

  item_type: ItemTypeExtended
  item_id: int

  action: EmitAction
  callback: Optional[Callback]

