print(">>>>>> import routers.py ...")
from fastapi import APIRouter, Security
# from ..core.config import settings

from . import (
  # routers_items,

  routers_tablemetas,
  routers_datasets,
  routers_workspaces,
  routers_users,

  routers_posts,
  routers_comments
)

api_router = APIRouter()


api_router.include_router(
  routers_users.router,
  prefix="/users",
  tags=["users"]
)

api_router.include_router(
  routers_workspaces.router,
  prefix="/workspaces",
  tags=["workspaces"]
)

api_router.include_router(
  routers_datasets.router,
  prefix="/datasets",
  tags=["datasets"]
)

api_router.include_router(
  routers_tablemetas.router,
  prefix="/tables",
  tags=["tables"]
)


### tutorial routes

# api_router.include_router(
#   routers_items.router,
#   prefix="/items",
#   tags=["items"]
# )
api_router.include_router(
  routers_posts.router,
  prefix="/posts",
  tags=["posts"]
)
api_router.include_router(
  routers_comments.router,
  prefix="/comments",
  tags=["comments"]
)
