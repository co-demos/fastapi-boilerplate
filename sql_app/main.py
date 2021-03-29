from .core.config import settings

import databases

from .core.tags_metadata import tags_metadata

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_socketio import SocketManager

from .crud import crud_items, crud_users

from .models import (
  models_item,
  models_post,
  models_comment,
  models_user,
)

from .db.database import engine, database

models_item.Base.metadata.create_all(bind=engine)
models_post.Base.metadata.create_all(bind=engine)
models_comment.Base.metadata.create_all(bind=engine)
models_user.Base.metadata.create_all(bind=engine)

from .routers import (
  routers_items,
  routers_users,
  routers_posts,
  routers_comments
)

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
  routers_users.router,
  prefix="/users",
  tags=["users"]
)
app.include_router(
  routers_items.router,
  prefix="/items",
  tags=["items"]
)
app.include_router(
  routers_posts.router,
  prefix="/posts",
  tags=["posts"]
)
app.include_router(
  routers_comments.router,
  prefix="/comments",
  tags=["comments"]
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
