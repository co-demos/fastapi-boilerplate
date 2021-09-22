print(">>>>>> import routers.routers_tablemetas.py ...")

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from . import ( List, Session, APIRouter, Depends,
  HTTPException, status, BackgroundTasks,
  get_db, Query
)

import uuid

from fastapi.encoders import jsonable_encoder

from ..schemas.schemas_tablemeta import (
  Tablemeta,
  TablemetaBase,
  TablemetaCreate,
  TablemetaData,
  TablemetaUpdate,
  TablemetaList,

  TabledataUpdateCell,
  TabledataUpdateRow,
  TabledataAddRow,
  TabledataDeleteRow,
  TabledataUpdateRows,
)
from ..crud.crud_tablemetas import tablemeta

from ..schemas.schemas_invitation import InvitationToTablemeta

from ..models.models_user import User
from ..crud.crud_users import (
  get_current_user,
  get_current_active_user,
)
from ..models.models_tabledata import TableDataBuilder, CreateFieldsCodes

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

  print("\n... === create_tablemeta_for_user > dataset_id :", dataset_id)
  # print("\n... === create_tablemeta_for_user > obj_in :", obj_in)
  # print("\n... === create_tablemeta_for_user > obj_in.dict() ... " )
  # pp.pprint(obj_in.dict())

  ### === TABLE DATA ===

  ### 1a/ set up raw data and fields for later
  table_fields = obj_in.table_fields
  table_fields_dict = CreateFieldsCodes( [ field.dict() for field in table_fields ] )
  # print("\n... === create_tablemeta_for_user > table_fields ...")
  # pp.pprint(table_fields)
  # print("\n... === create_tablemeta_for_user > table_fields_dict ...")
  # pp.pprint(table_fields_dict)

  table_data = obj_in.table_data
  # print("\n... === create_tablemeta_for_user > table_data ...")
  # pp.pprint(table_data)

  ### 1b/ create an uuid with a prefix for alembic exclusion
  table_data_uuid = uuid.uuid4().hex
  print("\n... === create_tablemeta_for_user > table_data_uuid : ", table_data_uuid)

  ### 1c/ create table class with table_fields, table_data_uuid, table_data
  table_db_class = TableDataBuilder(
    db,
    table_data_uuid,
    table_fields_dict,
  )
  # print("\n... === create_tablemeta_for_user > table_db_class.table_fields ...")
  # pp.pprint(table_db_class.table_fields)

  ### 1d/ build Table object
  table_db_class.create_table()

  ### 1f/ populate table_db with data
  table_db_class.bulk_import(table_data)


  ### === TABLE METADATA ===

  ### 2a/ append dataset_id to obj_in TablemetaCreate
  obj_in.dataset_id = dataset_id
  obj_in.table_fields = table_fields_dict
  # print("\n... === create_tablemeta_for_user > obj_in.dict() ... " )
  # pp.pprint( obj_in.dict() )

  ### 2b/ convert obj_in to a dict
  obj_filtered = jsonable_encoder(obj_in)
  # print("\n... === create_tablemeta_for_user > obj_filtered ...")
  # pp.pprint(obj_filtered)

  ### 2d/ replace table_data by table_data identifier
  obj_filtered["table_data_uuid"] = table_data_uuid

  ### 2e/ format obj_filtered with TablemetaBase model
  new_obj_in = TablemetaData(**obj_filtered)
  # print("... === create_tablemeta_for_user > new_obj_in :", new_obj_in)

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
  tablemeta_in_db = tablemeta.get_by_id(db=db, id=obj_id, user=current_user)
  # if tablemeta_in_db is None:
  #   raise HTTPException(
  #     status_code=status.HTTP_404_NOT_FOUND,
  #     detail="tablemeta not found"
  # )
  return tablemeta_in_db


@router.get("/{obj_id}/data",
  summary="Get a tablemeta's data",
  description="Get a tablemeta's data by its id",
  )
  # response_model=Tablemeta
def read_tablemeta_data(
  obj_id: int,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  # tablemeta_data_in_db = tablemeta.get_table_data(db=db, tablemeta_id=obj_id, user=current_user)
  tablemeta_data_in_db = tablemeta.get_table_data(db=db, tablemeta_id=obj_id, user=current_user)
  # if tablemeta_data_in_db is None:
  #   raise HTTPException(
  #     status_code=status.HTTP_404_NOT_FOUND,
  #     detail="tablemeta not found"
  # )

  print("\n...read_tablemeta_data > tablemeta_data_in_db ... " )
  print( tablemeta_data_in_db )

  return tablemeta_data_in_db


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
  tablemeta_in_db = tablemeta.get_by_id(db, id=obj_id, user=current_user)
  # if tablemeta_in_db is None:
  #   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tablemeta not found")
  ### only owner and superuser for now
  ### need to check group and scope !!!
  # if not current_user.is_superuser and (tablemeta_in_db.owner_id != current_user.id):
  #   raise HTTPException(status_code=400, detail="Not enough permissions")
  tablemeta_in_db = tablemeta.update(db=db, db_obj=tablemeta_in_db, obj_in=obj_in)
  return tablemeta_in_db


@router.put("/{obj_id}/data",
  summary="Update a tablemeta's data row or rows",
  description="Update a tablemeta's data row by its id",
  )
def update_tablemeta_data(
  obj_id: int,
  obj_in: Union[TabledataUpdateCell, TabledataUpdateRow, TabledataAddRow, TabledataUpdateRows],
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  tablemeta_in_db = tablemeta.get_by_id(db, id=obj_id, user=current_user, req_type="write")
  # if tablemeta_in_db is None:
  #   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tablemeta not found")
  if not current_user.is_superuser and (tablemeta_in_db.owner_id != current_user.id):
    raise HTTPException(status_code=400, detail="Not enough permissions")
  tablemeta_data_in_db = tablemeta.update_table_data_row(db=db, tablemeta_id=obj_id, obj_in=obj_in)
  if tablemeta_data_in_db is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="tablemeta's data not found"
  )
  print("\n...update_tablemeta_data > tablemeta_data_in_db ... " )
  print( tablemeta_data_in_db )

  return tablemeta_data_in_db


@router.post("/{obj_id}/invite",
  summary="Invite people to a tablemeta",
  description="Invite a list of users or mails to a tablemeta",
  response_model=Tablemeta
  )
async def invite_to_tablemeta(
  obj_id: int,
  obj_in: InvitationToTablemeta,
  background_tasks: BackgroundTasks,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  tablemeta_in_db = tablemeta.get_by_id(db=db, id=obj_id, user=current_user, req_type="manage")
  # if tablemeta_in_db is None:
  #   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tablemeta not found")
  ### only owner and superuser for now
  ### need to check group and scope !!!
  # if not current_user.is_superuser and (tablemeta_in_db.owner_id != current_user.id):
  #   raise HTTPException(status_code=400, detail="Not enough permissions")

  tablemeta_in_db = tablemeta.invite(
    db=db,
    background_tasks=background_tasks,
    db_obj=tablemeta_in_db,
    obj_in=obj_in,
    invitor=current_user
  )
  return tablemeta_in_db


@router.delete("/{obj_id}/data",
  summary="Delete a tablemeta's data row or rows",
  description="Delete a tablemeta's data row by its id",
  )
def delete_tablemeta_data(
  obj_id: int,
  obj_in: TabledataDeleteRow,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  print("\n...delete_tablemeta_data > obj_id : ", obj_id )
  print("...delete_tablemeta_data > obj_in : ", obj_in )
  tablemeta_in_db = tablemeta.get_by_id(db, id=obj_id, user=current_user, req_type="manage")
  # if tablemeta_in_db is None:
  #   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tablemeta not found")
  # if not current_user.is_superuser and (tablemeta_in_db.owner_id != current_user.id):
  #   raise HTTPException(status_code=400, detail="Not enough permissions")
  tablemeta_data_in_db = tablemeta.remove_table_data_row(db=db, tablemeta_id=obj_id, obj_in=obj_in)
  print("\n...delete_tablemeta_data > tablemeta_data_in_db ... " )
  print( tablemeta_data_in_db )

  return tablemeta_data_in_db


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
