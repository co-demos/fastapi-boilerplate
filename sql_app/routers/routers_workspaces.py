print(">>>>>> import routers.routers_workspaces.py ...")

from . import ( List, Session, APIRouter, Depends,
  HTTPException, status, BackgroundTasks,
  get_db, Query
)

from typing import Optional

from ..schemas.schemas_workspace import Workspace, WorkspaceCreate, WorkspaceUpdate, WorkspaceList
from ..crud.crud_workspaces import workspace

from ..schemas.schemas_invitation import InvitationToWorkspace

from ..models.models_user import User
from ..crud.crud_users import user
from ..crud.crud_users import (
  get_current_user,
  get_current_user_optional,
  get_current_active_user,
)


router = APIRouter()


@router.post("/",
  summary="Create an workspace",
  description="Create an workspace, including the id of the user creating the workspace",
  response_model=Workspace,
  status_code=status.HTTP_201_CREATED
  )
def create_workspace_for_user(
  obj_in: WorkspaceCreate,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  user_id = current_user.id
  return workspace.create_with_owner(db=db, obj_in=obj_in, owner_id=user_id)


@router.get("/{obj_id}",
  summary="Get a workspace",
  description="Get a workspace by its id - authentication is optional",
  response_model=Workspace,
  )
def read_workspace(
  obj_id: int, 
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user_optional)
  ):
  workspace_in_db = workspace.get_by_id(db, id=obj_id, user=current_user, req_type="read")
  return workspace_in_db


@router.put("/{obj_id}",
  summary="Update a workspace",
  description="Update a workspace by its id",
  response_model=Workspace
  )
def update_workspace(
  obj_id: int,
  obj_in: WorkspaceUpdate,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  workspace_in_db = workspace.get_by_id(db=db, id=obj_id, user=current_user, req_type="write")
  workspace_in_db = workspace.update(db=db, db_obj=workspace_in_db, obj_in=obj_in)
  return workspace_in_db


@router.post("/{obj_id}/invite",
  summary="Invite people to a workspace",
  description="Invite a list of users or mails to a workspace",
  response_model=Workspace
  )
async def invite_to_workspace(
  obj_id: int,
  obj_in: InvitationToWorkspace,
  background_tasks: BackgroundTasks,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  workspace_in_db = workspace.get_by_id(db=db, id=obj_id, user=current_user, req_type="manage")
  workspace_in_db = workspace.invite(
    db=db,
    background_tasks=background_tasks,
    db_obj=workspace_in_db,
    obj_in=obj_in,
    invitor=current_user
  )
  return workspace_in_db


@router.get("/",
  summary="Get a list of all workspaces",
  description="Get all workspaces given a limit",
  response_model=List[Workspace]
  )
def read_workspaces(
  skip: int = 0, limit: int = 100, 
  current_user: User = Depends(get_current_user_optional),
  db: Session = Depends(get_db),
  ):
  workspaces = workspace.get_multi(db=db, skip=skip, limit=limit, user=current_user, req_type="read")
  return workspaces


@router.delete("/{obj_id}",
  summary="Delete a workspace",
  description="Delete a workspace by its id",
  response_model=Workspace
  )
def delete_workspace(
  obj_id: int,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  print("delete_workspace > obj_id : ", obj_id)
  workspace_deleted = workspace.remove(db=db, id=obj_id, current_user=current_user)
  print("delete_workspace > workspace_deleted : ", workspace_deleted)
  return workspace_deleted
