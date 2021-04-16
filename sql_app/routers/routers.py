from fastapi import APIRouter
# from ..core.config import settings

from . import (
  routers_items,
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
  routers_items.router,
  prefix="/items",
  tags=["items"]
)
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
