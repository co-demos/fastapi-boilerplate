print(">>>>>> import routers.routers_searches.py ...")

from . import ( List, Session, APIRouter, Depends,
  HTTPException, status,
  get_db, Query
)

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import parse_obj_as

from ..schemas.schemas_choices import PermissionType, ItemTypes, OperatorType

from ..schemas.schemas_user import UsersList
from ..schemas.schemas_group import GroupsList
from ..schemas.schemas_workspace import WorkspacesList
from ..schemas.schemas_dataset import DatasetsList
from ..schemas.schemas_tablemeta import TablemetasList

from ..models.models_user import User

from ..crud.crud_users import user
from ..crud.crud_groups import group
from ..crud.crud_workspaces import workspace
from ..crud.crud_datasets import dataset
from ..crud.crud_tablemetas import tablemeta

from ..crud.crud_users import (
  get_current_user,
  get_current_active_user,
)

router = APIRouter()

ITEM_TYPES = {
  "users": {
    "crud": user,
    "model": UsersList,
    "fields": ["email", "name", "surname", "username", "description"],
  },
  "groups": {
    "crud": group,
    "model": GroupsList,
    "fields": ["title", "description"],
  },
  "workspaces": {
    "crud": workspace,
    "model": WorkspacesList,
    "fields": ["title", "description"],
  },
  "datasets": {
    "crud": dataset,
    "model": DatasetsList,
    "fields": ["title", "description"],
  },
  "tables": {
    "crud": tablemeta,
    "model": TablemetasList,
    "fields": ["title", "description"],
  },
}

@router.get("/by_type/{item_type}",
  summary="Search for items by type",
  description="Get items given a type and a query",
  # response_model=List[ITEM_TYPES[item_type]["model"]]
  )
async def search_by_type(
  q: str = Query("", min_length=3),
  item_type: ItemTypes = ItemTypes.groups,
  auth_type: PermissionType = Query([PermissionType.perm_public]),
  operator: OperatorType = OperatorType.or_,
  skip: int = 0, limit: int = 100, 
  current_user: User = Depends(get_current_user),
  db: Session = Depends(get_db),
  ):
  print("\nsearch_by_type > q : ", q)
  print("search_by_type > item_type : ", item_type)
  print("search_by_type > operator : ", operator)

  items_in_db = ITEM_TYPES[item_type]["crud"].search_multi_by_fields(
    db=db,
    q=q,
    fields=ITEM_TYPES[item_type]["fields"],
    auth_level=auth_type,
    operator=operator, 
  )
  print("search_by_type > items_in_db : ", items_in_db)
  return items_in_db


@router.get("/any",
  summary="Search any item ",
  description="Get items given a string query",
  )
async def search_any(
  q: str = Query("", min_length=3),
  item_types: List[ItemTypes] = Query([ItemTypes.groups]),
  auth_type: PermissionType = Query([PermissionType.perm_public]),
  operator: OperatorType = OperatorType.or_,
  skip: int = 0, limit: int = 100, 
  current_user: User = Depends(get_current_user),
  db: Session = Depends(get_db),
  ):
  print("\nsearch_any > q : ", q)
  print("search_any > item_types : ", item_types)
  print("search_any > operator : ", operator)

  results = {}
  for item_type in item_types :
    items_in_db, count = ITEM_TYPES[item_type]["crud"].search_multi_by_fields(
      db=db,
      q=q,
      fields=ITEM_TYPES[item_type]["fields"],
      auth_level=auth_type,
      operator=operator, 
    )
    # print("search_any > items_in_db : ", items_in_db)
    items_results = {}
    # print("search_any > jsonable_encoder(items_in_db) : ", jsonable_encoder(items_in_db))
    model = ITEM_TYPES[item_type]["model"]
    print("search_any > model : ", model)
    
    items_results["results"] = model.parse_obj(jsonable_encoder(items_in_db))
    items_results["count"] = count
    
    results[item_type] = items_results

  # print("search_any > results : ", results)
  # return JSONResponse(content=results)
  return results
