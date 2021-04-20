print(">>>>>> import schemas_message.py >  Msg ...")
from pydantic import BaseModel

class Msg(BaseModel):
  msg: str
