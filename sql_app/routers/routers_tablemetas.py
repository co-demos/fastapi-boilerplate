from . import ( List, Session, APIRouter, Depends,
  HTTPException, status,
  get_db,
)

import uuid

from fastapi.encoders import jsonable_encoder

from ..schemas.schemas_tablemeta import Tablemeta, TablemetaBase, TablemetaCreate, TablemetaData, TablemetaUpdate, TablemetaList
from ..crud.crud_tablemetas import tablemeta

from ..models.models_user import User
from ..crud.crud_users import (
  get_current_user,
  get_current_active_user,
)

import pprint
pp = pprint.PrettyPrinter(indent=1)

router = APIRouter()


@router.post("/{dataset_id}",
  summary="Create an tablemeta",
  description="Create an tablemeta, including the id of the user creating the tablemeta",
  response_model=Tablemeta,
  status_code=status.HTTP_201_CREATED
)
def create_tablemeta_for_user(
  dataset_id: int,
  obj_in: TablemetaCreate,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  user_id = current_user.id

  # print("\n... === create_tablemeta_for_user > dataset_id :", dataset_id)
  # print("\n... === create_tablemeta_for_user > obj_in :", obj_in)
  # print("\n... === create_tablemeta_for_user > obj_in.dict() ... " )
  # pp.pprint(obj_in.dict())

  ### === TABLE DATA ===
  ### 1/ dynamically create table with table_fields, table_data, table_data_uuid
  table_fields = obj_in.table_fields
  print("\n... === create_tablemeta_for_user > table_fields ...")
  pp.pprint(table_fields)

  table_data = obj_in.table_data
  print("\n... === create_tablemeta_for_user > table_data ...")
  pp.pprint(table_data)

  table_data_uuid = uuid.uuid4().hex
  print("\n... === create_tablemeta_for_user > table_data_uuid : ", table_data_uuid)


  ### === TABLE METADATA ===
  ### 2a/ append dataset_id to obj_in TablemetaCreate
  obj_in.dataset_id = dataset_id
  print("\n... === create_tablemeta_for_user > obj_in.dict() ... " )
  pp.pprint( obj_in.dict() )

  ### 2b/ convert obj_in to a dict
  obj_filtered = jsonable_encoder(obj_in)
  print("\n... === create_tablemeta_for_user > obj_filtered ...")
  pp.pprint(obj_filtered)

  ### 2d/ replace table_data by table_data identifier
  obj_filtered["table_data_uuid"] = table_data_uuid

  ### 2e/ format obj_filtered with TablemetaBase model
  new_obj_in = TablemetaData(**obj_filtered)
  print("... === create_tablemeta_for_user > new_obj_in :", new_obj_in)

  ### 3/ create tablemeta in postgresql  and return result 
  return tablemeta.create_with_owner(db=db, obj_in=new_obj_in, owner_id=user_id)


@router.get("/{obj_id}",
  summary="Get a tablemeta",
  description="Get a tablemeta by its id",
  response_model=Tablemeta
  )
def read_tablemeta(
  obj_id: int,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  tablemeta_in_db = tablemeta.get_by_id(db=db, id=obj_id)
  if tablemeta_in_db is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="tablemeta not found"
  )
  return tablemeta_in_db


@router.put("/{obj_id}",
  summary="update a tablemeta",
  description="update a tablemeta by its id",
  response_model=Tablemeta
  )
def update_tablemeta(
  obj_id: int,
  obj_in: TablemetaUpdate,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  tablemeta_in_db = tablemeta.get_by_id(db, id=obj_id)
  if tablemeta_in_db is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tablemeta not found")
  ### only owner and superuser for now
  ### need to check group and scope !!!
  if not current_user.is_superuser and (tablemeta_in_db.owner_id != current_user.id):
    raise HTTPException(status_code=400, detail="Not enough permissions")
  tablemeta_in_db = tablemeta.update(db=db, db_obj=tablemeta_in_db, obj_in=obj_in)
  return tablemeta_in_db


@router.get("/dataset/{dataset_id}",
  summary="Get a list of all tablemetas for a dataset",
  description="Get all tablemetas of a dataset given and a limit",
  response_model=List[Tablemeta]
)
def read_tablemetas(
  dataset_id: int,
  skip: int = 0, limit: int = 100,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user),
  ):
  print("\n...read_tablemetas > current_user :", current_user )
  print("...read_tablemetas > dataset_id :", dataset_id )
  tablemetas = tablemeta.get_multi_by_dataset(db=db, dataset_id=dataset_id, skip=skip, limit=limit)
  return tablemetas


@router.delete("/{obj_id}",
  summary="Delete a tablemeta",
  description="Delete a tablemeta by its id",
  response_model=Tablemeta
  )
def delete_tablemeta(
  obj_id: int,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  print("delete_tablemeta > obj_id : ", obj_id)
  tablemeta_deleted = tablemeta.remove(db=db, id=obj_id, current_user=current_user)
  print("delete_tablemeta > tablemeta_deleted : ", tablemeta_deleted)
  return tablemeta_deleted