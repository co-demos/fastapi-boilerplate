print(">>>>>> import routers.routers.py ...")

from fastapi import APIRouter, Security
# from ..core.config import settings

from . import (
  # routers_items,

  routers_tablemetas,
  routers_datasets,
  routers_workspaces,
  routers_users,
  routers_groups,
  routers_invitations,
  routers_searches,

  routers_comments,

)

api_router = APIRouter()


api_router.include_router(
  routers_users.router,
  prefix="/users",
  tags=["users"]
)

api_router.include_router(
  routers_searches.router,
  prefix="/searches",
  tags=["searches"]
)

api_router.include_router(
  routers_invitations.router,
  prefix="/invitations",
  tags=["invitations"]
)

api_router.include_router(
  routers_groups.router,
  prefix="/groups",
  tags=["groups"]
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

api_router.include_router(
  routers_comments.router,
  prefix="/comments",
  tags=["comments"]
)


### tutorial routes

# api_router.include_router(
#   routers_items.router,
#   prefix="/items",
#   tags=["items"]
# )
# api_router.include_router(
#   routers_posts.router,
#   prefix="/posts",
#   tags=["posts"]
# )

