from . import ( List, Session, APIRouter, Depends,
  HTTPException, status,
  get_db,
)

from ..schemas.schemas_sockets import CreateOwnRoom, BroadcastAction

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
async def io_connect( sid, environ ):
  print("\nio_connect > sid : ", sid)
  print("io_connect > environ : ", environ)
  await sio.emit('handshake', { 'sid': sid })

@sio.on("disconnect")
async def io_connect( sid ):
  print("\nio_disconnect > sid : ", sid)


# @router.sio.on('*')
# @app.sio.on('*')
# async def io_catch_all(sid, data):
#   print("\nio_catch_all > sid : ", sid)


@sio.on("join_own_room")
async def io_join_own_room(
  sid,
  data: CreateOwnRoom,
  ):
  print("\njoin_own_room > sid : ", sid)
  print("join_own_room > data : ", data)
  user_email = data["user_email"]
  print("join_own_room > user_email : ", user_email)

  ## create own room for user
  sio.enter_room( sid, user_email )
  await sio.emit('own_room', f'room created for : {user_email}')


@sio.on("broadcast_action")
async def io_broadcast_action(
  sid,
  data: BroadcastAction,
  ):
  print("\nbroadcast_action > sid : ", sid)
  print("broadcast_action > data : ", data)

  from_user_email = data["from_user_email"]
  rooms = data["target_rooms"]
  data = "tadaaaa"

  ## broadcast msg room to user
  await sio.emit('action_message', data, to=rooms, skip_sid=sid)


# @sio.on("join")
# async def io_join(
#   sid,
#   *args, **kwargs
#   ):
#   print("\nio_join > sid : ", sid)
#   print("io_join > args : ", args)
#   print("io_join > kwargs : ", kwargs)
#   ## authenticate / get user 


# @router.sio.on("chat_test", namespace="/chat")
# @sio.on("chat_test", namespace="/chat")
# async def io_chat_test(
#   sid,
#   data
#   ):
#   await app.sio.emit('test_sio_chat_resp', 'Testing socket ok - namespace chat')
