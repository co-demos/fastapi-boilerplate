print(">>>>>> import schemas_message.py >  Msg ...")
from pydantic import BaseModel

class Msg(BaseModel):
  item_type: str = "message"
  msg: str
