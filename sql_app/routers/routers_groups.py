from . import ( List, Session, APIRouter, Depends,
  HTTPException, status, BackgroundTasks,
  get_db, Query
)

from fastapi.encoders import jsonable_encoder
from ..schemas.schemas_group import UserInDBBaseLight, Group, GroupCreate, GroupUpdate, GroupList
from ..crud.crud_groups import group

from ..schemas.schemas_invitation import InvitationToGroup

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
async def create_group_for_user(
  obj_in: GroupCreate,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  user_id = current_user.id
  
  members_registred = [current_user]
  members_pending = []
  for email in obj_in.pending_users:
    user_in_db = user.get_user_by_email(db, email=email)
    if user_in_db is None:
      members_pending.append(email)
    else: 
      members_registred.append(user_in_db)

  return group.create_with_owner_in_team(
    db=db,
    obj_in=obj_in,
    owner_id=user_id,
    users=members_registred,
    pending_users=members_pending
  )


@router.get("/{obj_id}",
  summary="Get a group",
  description="Get a group by its id",
  response_model=Group,
  )
async def read_group(
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
async def update_group(
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


@router.post("/{obj_id}/invite",
  summary="Invite people to a group",
  description="Invite a list of users or mails to a group",
  response_model=Group
  )
async def invite_to_group(
  obj_id: int,
  obj_in: InvitationToGroup,
  background_tasks: BackgroundTasks,
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

  group_in_db = group.invite(
    db=db,
    background_tasks=background_tasks,
    db_obj=group_in_db,
    obj_in=obj_in,
    invitor=current_user
  )
  return group_in_db


@router.get("/",
  summary="Get a list of all groups",
  description="Get all groups given a limit",
  response_model=List[Group]
  )
async def read_groups(
  skip: int = 0, limit: int = 100, 
  current_user: User = Depends(get_current_user),
  db: Session = Depends(get_db),
  ):
  groups = group.get_multi(db=db, skip=skip, limit=limit)
  return groups


# @router.get("/search/",
#   summary="Search for a list of groups",
#   description="Get groups given a string query",
#   response_model=List[Group]
#   )
# async def search_groups(
#   q: str = Query("fixedquery", min_length=3),
#   skip: int = 0, limit: int = 100, 
#   current_user: User = Depends(get_current_user),
#   db: Session = Depends(get_db),
#   ):
#   groups_in_db = group.search_multi_by_fields(
#     db=db,
#     q=q,
#     fields=["title", "description"],
#   )
#   return groups_in_db


@router.delete("/{obj_id}",
  summary="Delete a group",
  description="Delete a group by its id",
  response_model=Group
  )
async def delete_group(
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
