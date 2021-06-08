from . import ( List, Session, APIRouter, Depends,
  HTTPException, status,
  get_db, Query
)

from fastapi.encoders import jsonable_encoder

from ..schemas.schemas_dataset import Dataset, DatasetBase, DatasetCreate, DatasetUpdate, DatasetList
from ..crud.crud_datasets import dataset

from ..schemas.schemas_invitation import InvitationToDataset

from ..models.models_user import User
from ..crud.crud_users import (
  get_current_user,
  get_current_active_user,
)

from ..routers.routers_tablemetas import (
  create_tablemeta_for_user,
  read_tablemeta_data
)

import pprint
pp = pprint.PrettyPrinter(indent=1)

router = APIRouter()


@router.post(
  "/",
  summary="Create an dataset",
  description="Create an dataset, including the id of the user creating the dataset",
  response_model=Dataset,
  status_code=status.HTTP_201_CREATED
  )
def create_dataset_for_user(
  obj_in: DatasetCreate,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  user_id = current_user.id

  # print("\n...create_dataset_for_user > obj_in :", obj_in)
  # print("\n...create_dataset_for_user > obj_in.dict() ... " )
  # pp.pprint(obj_in.dict()) 

  ### 1/ create dataset to get dataset id, without table data
  obj_filtered = jsonable_encoder(obj_in)
  # print("\n...create_dataset_for_user > obj_filtered :", obj_filtered)
  new_obj_in = DatasetBase(**obj_filtered)
  # print("\n...create_dataset_for_user > new_obj_in :", new_obj_in)
  new_dataset = dataset.create_with_owner(db=db, obj_in=new_obj_in, owner_id=user_id)
  # print("\n...create_dataset_for_user > new_dataset :", new_dataset)
  new_dataset_id = new_dataset.id
  # print("\n...create_dataset_for_user > new_dataset_id :", new_dataset_id)

  ### 2/ create table_metadata
  print("\n...create_dataset_for_user > tables ... " )
  tables = obj_in.tables
  tablemeta_ids = {
    "tables": []
  }
  for table in tables :

    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ ")

    ### 2a/ append dataset id to table_metadata and create table_meta
    new_table_meta = create_tablemeta_for_user(new_dataset_id, table, db, current_user)
    print("\n...create_dataset_for_user > new_table_meta ... ", new_table_meta )
    # print("\n...create_dataset_for_user > new_table_meta ... " )
    # pp.pprint( new_table_meta ) 

    ### 2b/ store table_meta.id for later
    tablemeta_ids["tables"].append(new_table_meta.id)

  ### 3b/ return new_dataset
  return new_dataset


@router.get("/{obj_id}",
  summary="Get a dataset",
  description="Get a dataset by its id",
  response_model=Dataset
  )
def read_dataset(
  obj_id: int,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  dataset_in_db = dataset.get_by_id(db=db, id=obj_id)
  if dataset_in_db is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="dataset not found"
  )

  print("\n...read_dataset > dataset_in_db ... " )
  pp.pprint( dataset_in_db )

  return dataset_in_db


@router.put("/{obj_id}",
  summary="update a dataset",
  description="update a dataset by its id",
  response_model=Dataset
  )
def update_dataset(
  obj_id: int,
  obj_in: DatasetUpdate,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  dataset_in_db = dataset.get_by_id(db, id=obj_id)
  if dataset_in_db is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dataset not found")
  ### only owner and superuser for now
  ### need to check group and scope !!!
  if not current_user.is_superuser and (dataset_in_db.owner_id != current_user.id):
    raise HTTPException(status_code=400, detail="Not enough permissions")
  dataset_in_db = dataset.update(db=db, db_obj=dataset_in_db, obj_in=obj_in)
  return dataset_in_db


@router.post("/{obj_id}/invite",
  summary="Invite people to a dataset",
  description="Invite a list of users or mails to a dataset",
  response_model=Dataset
  )
async def invite_to_dataset(
  obj_id: int,
  obj_in: InvitationToDataset,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  dataset_in_db = dataset.get_by_id(db=db, id=obj_id)
  if dataset_in_db is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dataset not found")
  ### only owner and superuser for now
  ### need to check group and scope !!!
  if not current_user.is_superuser and (dataset_in_db.owner_id != current_user.id):
    raise HTTPException(status_code=400, detail="Not enough permissions")

  dataset_in_db = dataset.invite(db=db, db_obj=dataset_in_db, obj_in=obj_in)
  return dataset_in_db


@router.get("/",
  summary="Get a list of all datasets",
  description="Get all datasets given a limit",
  response_model=List[Dataset]
  )
def read_datasets(
  skip: int = 0, limit: int = 100,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user),
  ):
  datasets = dataset.get_multi(db=db, skip=skip, limit=limit)
  return datasets


@router.delete("/{obj_id}",
  summary="Delete a dataset",
  description="Delete a dataset by its id",
  response_model=Dataset
  )
def delete_dataset(
  obj_id: int,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  print("delete_dataset > obj_id : ", obj_id)
  dataset_deleted = dataset.remove(db=db, id=obj_id, current_user=current_user)
  print("delete_dataset > dataset_deleted : ", dataset_deleted)
  return dataset_deleted
