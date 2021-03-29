import databases
from pathlib import Path

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_socketio import SocketManager

from .core.config import settings
from .core.tags_metadata import tags_metadata

from .crud import crud_items, crud_users

from .db.database import engine, database
from .models import (
  models_item,
  models_post,
  models_comment,
  models_user,
)

models_item.Base.metadata.create_all(bind=engine)
models_post.Base.metadata.create_all(bind=engine)
models_comment.Base.metadata.create_all(bind=engine)
models_user.Base.metadata.create_all(bind=engine)


from .routers.routers import api_router

app = FastAPI(
  title=settings.APP_TITLE,
  description=settings.APP_DESCRIPTION,
  version=settings.APP_VERSION,
  openapi_tags=tags_metadata
)


### SOCKET IO

# cf : https://pypi.org/project/fastapi-socketio/
socket_manager = SocketManager(app=app)


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


### ROUTERS
app.include_router(
  api_router,
  # prefix=settings.API_V1_STR
)


### databases related

@app.on_event("startup")
async def startup():
  print("startup app > ...")
  await database.connect()

@app.on_event("shutdown")
async def shutdown():
  print("shutdown app > ...")
  await database.disconnect()


### STATIC FILES

# cf : https://www.starlette.io/staticfiles/
current_file = Path(__file__)
project_root = current_file.parent
project_root_absolute = project_root.resolve()
static_root_absolute = project_root_absolute / "static"
app.mount("/static", StaticFiles(directory=static_root_absolute), name="static")
