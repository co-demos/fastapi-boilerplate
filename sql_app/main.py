# import databases
from pathlib import Path

import pprint
pp = pprint.PrettyPrinter(indent=1)

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi

from .core.config import settings
from .core.tags_metadata import tags_metadata

import socketio
# from fastapi_socketio import SocketManager
# from .websockets import SocketManager

from .db.database import engine_commons, database_commons, database_data
from .db.base_class import BaseCommons

# from .models import (
  
#   ### tutorial modells
#   models_item,
#   models_post,
#   models_comment,

#   ### data patch models
#   models_licence,
#   models_tablemeta,
#   models_dataset,
#   models_workspace,
#   models_user,
# )

### tutorial models
# models_item.Base.metadata.create_all(bind=engine_commons)
# models_post.Base.metadata.create_all(bind=engine_commons)
# models_comment.Base.metadata.create_all(bind=engine_commons)

### data patch models
# models_licence.Base.metadata.create_all(bind=engine_commons)
# models_tablemeta.Base.metadata.create_all(bind=engine_commons)
# models_dataset.Base.metadata.create_all(bind=engine_commons)
# models_workspace.Base.metadata.create_all(bind=engine_commons)
# models_user.Base.metadata.create_all(bind=engine_commons)

BaseCommons.metadata.create_all(bind=engine_commons)

app = FastAPI(
  title=settings.APP_TITLE,
  description=settings.APP_DESCRIPTION,
  version=settings.APP_VERSION,
  openapi_tags=tags_metadata,
  # openapi_prefix=settings.API_V1_STR,
  docs_url=f"{settings.API_V1_STR}/docs",
  redoc_url=f"{settings.API_V1_STR}/redoc",
  debug=True
)
print("\nmain.py > app : ", app.__dict__)


### CORS

origins = [
  "*",
  # "http://localhost",
  # "http://localhost:8000",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

### SOCKET IO

# cf : https://pypi.org/project/fastapi-socketio/
# socket_manager = SocketManager(
#   app=app,
#   mount_location = "/ws",
#   socketio_path = "socket.io",
#   cors_allowed_origins=origins
# )
# print("\nmain.py > socket_manager : ", socket_manager.__dict__)

sio = socketio.AsyncServer(
    # async_mode='asgi',
    # cors_allowed_origins='*'
    async_mode='asgi',
    cors_allowed_origins=[]
)
subapi = socketio.ASGIApp(
    socketio_server=sio,
    other_asgi_app=app,
    socketio_path='/socket.io'
)
app.mount("/ws", subapi)



### ROUTERS

from .routers.routers import api_router

app.include_router(
  api_router,
  prefix=settings.API_V1_STR
)

from .websockets.routers_websockets import *


### OPENAPI

def custom_openapi():
  if app.openapi_schema:
    return app.openapi_schema
  openapi_schema = get_openapi(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    routes=app.routes,
  )
  openapi_schema["info"]["x-logo"] = {
    "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
  }
  # print ("openapi_schema : ...") 
  # pp.pprint( openapi_schema.keys() )
  # pp.pprint( openapi_schema )

  # print ("\nopenapi_schema.info : ...") 
  # pp.pprint( openapi_schema['info'] )

  # print ("\nopenapi_schema.openapi : ...") 
  # pp.pprint( openapi_schema['openapi'] )

  # print ("\nopenapi_schema.openapi : ...") 
  # pp.pprint( openapi_schema['components'] )

  app.openapi_schema = openapi_schema
  return app.openapi_schema

app.openapi = custom_openapi



### databases related

@app.on_event("startup")
async def startup():
  print("....... startup > database_data.connect() > startup app ...")
  await database_data.connect()

@app.on_event("shutdown")
async def shutdown():
  print("....... startup > database_data.connect() > shutdown app ...")
  await database_data.disconnect()


### STATIC FILES

# cf : https://www.starlette.io/staticfiles/
current_file = Path(__file__)
project_root = current_file.parent
project_root_absolute = project_root.resolve()
static_root_absolute = project_root_absolute / "static"
app.mount("/static", StaticFiles(directory=static_root_absolute), name="static")
