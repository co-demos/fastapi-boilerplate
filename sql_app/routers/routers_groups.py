from . import ( List, Session, APIRouter, Depends,
  HTTPException, status,
  get_db,
)

from fastapi.encoders import jsonable_encoder
from ..schemas.schemas_group import UserInDBBaseLight, Group, GroupCreate, GroupUpdate, GroupList
from ..crud.crud_groups import group

from ..models.models_user import User
from ..crud.crud_users import user
from ..crud.crud_users import (
  get_current_user,
  get_current_active_user,
)


router = APIRouter()


@router.post("/",
  summary="Create an group",
  description="Create an group, including the id of the user creating the group",
  response_model=Group,
  status_code=status.HTTP_201_CREATED
  )
def create_group_for_user(
  obj_in: GroupCreate,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  user_id = current_user.id
  current_user_data = jsonable_encoder(current_user)
  current_user_ = UserInDBBaseLight(**current_user_data)
  obj_in.users = [ current_user_ ]
  return group.create_with_owner(db=db, obj_in=obj_in, owner_id=user_id)


@router.get("/{obj_id}",
  summary="Get a group",
  description="Get a group by its id",
  response_model=Group,
  )
def read_group(
  obj_id: int, 
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  group_in_db = group.get_by_id(db, id=obj_id)
  if group_in_db is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="group not found")
  return group_in_db


@router.put("/{obj_id}",
  summary="Update a group",
  description="Update a group by its id",
  response_model=Group
  )
def update_group(
  obj_id: int,
  obj_in: GroupUpdate,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  group_in_db = group.get_by_id(db=db, id=obj_id)
  if group_in_db is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="group not found")
  ### only owner and superuser for now
  ### need to check group and scope !!!
  if not current_user.is_superuser and (group_in_db.owner_id != current_user.id):
    raise HTTPException(status_code=400, detail="Not enough permissions")
  group_in_db = group.update(db=db, db_obj=group_in_db, obj_in=obj_in)
  return group_in_db


@router.get("/",
  summary="Get a list of all groups",
  description="Get all groups given a limit",
  response_model=List[Group]
  )
def read_groups(
  skip: int = 0, limit: int = 100, 
  current_user: User = Depends(get_current_user),
  db: Session = Depends(get_db),
  ):
  groups = group.get_multi(db=db, skip=skip, limit=limit)
  return groups


@router.delete("/{obj_id}",
  summary="Delete a group",
  description="Delete a group by its id",
  response_model=Group
  )
def delete_group(
  obj_id: int,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  print("delete_group > obj_id : ", obj_id)
  # group_in_db = group.get_by_id(db=db, id=id)
  # print("delete_group > group_in_db : ", group_in_db)
  # if not group_in_db:
  #   raise HTTPException(status_code=404, detail="group not found")
  group_deleted = group.remove(db=db, id=obj_id, current_user=current_user)
  print("delete_group > group_deleted : ", group_deleted)
  return group_deleted