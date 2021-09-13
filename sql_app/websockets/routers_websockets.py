from . import ( List, Session, APIRouter, Depends,
  HTTPException, status,
  get_db,
)

from ..crud.crud_users import (
  get_current_user,
)

from ..main import sio

""" 
namespaces :

- notif => io related to notifications =>
- data => io related to data => collab on a schema | field | dataset | table | cell + comment
- global_chat : chat drawer =>
- workspace : io in workspace page => collab on a common workspace
- group : io in groups page => collab on a group

"""

# router = APIRouter()

@sio.on("connect")
async def io_connect(
  sid, environ
  ):
  print("\nio_connect > sid : ", sid)
  print("io_connect > environ : ", environ)
  # print("io_connect > sid : ", sid)
  await sio.emit('handshake', { 'sid': sid })

# @router.sio.on('*')
# @app.sio.on('*')
# async def io_catch_all(sid, data):
#   print("\nio_catch_all > sid : ", sid)


# @router.sio.on("connect")
# @app.sio.on("connect")
# @sio.on("connect")
# async def io_connect(
#   sid,
#   ):
#   print("\nio_connect > sid : ", sid)
#   await app.sio.emit('hello', sid)
#   # await app.sio.emit('test_sio_resp', 'Testing socket ok')


# @router.sio.on("join")
# @app.sio.on("join")
# @sio.on("join")
# async def io_join(
#   sid,
#   *args, **kwargs
#   ):
#   print("\nio_join > sid : ", sid)
#   print("io_join > args : ", args)
#   print("io_join > kwargs : ", kwargs)

# @router.sio.on("test")
# @sio.on("test")
# async def io_test(
#   sid,
#   data
#   ):
#   await app.sio.emit('test_sio_resp', 'Testing socket ok')


# @router.sio.on("chat_test", namespace="/chat")
# @sio.on("chat_test", namespace="/chat")
# async def io_chat_test(
#   sid,
#   data
#   ):
#   await app.sio.emit('test_sio_chat_resp', 'Testing socket ok - namespace chat')
