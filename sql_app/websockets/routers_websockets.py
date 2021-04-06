from . import ( List, Session, APIRouter, Depends,
  HTTPException, status,
  get_db,
)

from ..crud.crud_users import (
  get_current_user,
)

from ..main import app

""" 
namespaces :

- notif => io related to notifications =>
- data => io related to data => collab on a schema | field | dataset | table | cell + comment
- global_chat : chat drawer =>
- workspace : io in workspace page => collab on a common workspace
- group : io in groups page => collab on a group

"""


@app.sio.on("test")
async def io_test(
  sid,
  data
  ):
  await app.sio.emit('test_sio_resp', 'Testing socket ok')

@app.sio.on("chat_test", namespace="/chat")
async def io_chat_test(
  sid,
  data
  ):
  await app.sio.emit('test_sio_chat_resp', 'Testing socket ok - namespace chat')
