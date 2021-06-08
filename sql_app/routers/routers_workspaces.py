from . import ( List, Session, APIRouter, Depends,
  HTTPException, status,
  get_db, Query
)

from ..schemas.schemas_workspace import Workspace, WorkspaceCreate, WorkspaceUpdate, WorkspaceList
from ..crud.crud_workspaces import workspace

from ..schemas.schemas_invitation import InvitationToWorkspace

from ..models.models_user import User
from ..crud.crud_users import user
from ..crud.crud_users import (
  get_current_user,
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
  description="Get a workspace by its id",
  response_model=Workspace,
  )
def read_workspace(
  obj_id: int, 
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  workspace_in_db = workspace.get_by_id(db, id=obj_id)
  if workspace_in_db is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workspace not found")
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
  workspace_in_db = workspace.get_by_id(db=db, id=obj_id)
  if workspace_in_db is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workspace not found")
  ### only owner and superuser for now
  ### need to check group and scope !!!
  if not current_user.is_superuser and (workspace_in_db.owner_id != current_user.id):
    raise HTTPException(status_code=400, detail="Not enough permissions")
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
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  workspace_in_db = workspace.get_by_id(db=db, id=obj_id)
  if workspace_in_db is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workspace not found")
  ### only owner and superuser for now
  ### need to check workspace and scope !!!
  if not current_user.is_superuser and (workspace_in_db.owner_id != current_user.id):
    raise HTTPException(status_code=400, detail="Not enough permissions")

  workspace_in_db = workspace.invite(db=db, db_obj=workspace_in_db, obj_in=obj_in)
  return workspace_in_db


@router.get("/",
  summary="Get a list of all workspaces",
  description="Get all workspaces given a limit",
  response_model=List[Workspace]
  )
def read_workspaces(
  skip: int = 0, limit: int = 100, 
  current_user: User = Depends(get_current_user),
  db: Session = Depends(get_db),
  ):
  workspaces = workspace.get_multi(db=db, skip=skip, limit=limit)
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
  # workspace_in_db = workspace.get_by_id(db=db, id=id)
  # print("delete_workspace > workspace_in_db : ", workspace_in_db)
  # if not workspace_in_db:
  #   raise HTTPException(status_code=404, detail="workspace not found")
  workspace_deleted = workspace.remove(db=db, id=obj_id, current_user=current_user)
  print("delete_workspace > workspace_deleted : ", workspace_deleted)
  return workspace_deleted
