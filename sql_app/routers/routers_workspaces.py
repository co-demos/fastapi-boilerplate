print(">>>>>> import routers.routers_workspaces.py ...")

from . import ( List, Session, APIRouter, Depends,
  HTTPException, status, BackgroundTasks,
  get_db, Query
)

from typing import Optional

from ..schemas.schemas_workspace import Workspace, WorkspaceCreate, WorkspaceUpdate
from ..crud.crud_workspaces import workspace

from ..schemas.schemas_invitation import InvitationToWorkspace

from ..models.models_user import User
from ..crud.crud_users import user
from ..crud.crud_users import (
  get_current_user,
  get_current_user_optional,
  get_current_active_user,
)

from ..crud.crud_datasets import dataset

from ..schemas.schemas_comment import Comment, CommentWorkspace
from ..crud.crud_comments import comment

from ..schemas.schemas_patch import Patch, PatchWorkspace
from ..crud.crud_patches import patch

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


@router.get("/{obj_id}/datasets",
  summary="Get a workspace's datasets",
  description="Get a workspace's datasets by its id - authentication is optional",
  )
  # response_model=List[Dataset],
def read_workspace_datasets(
  obj_id: int, 
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user_optional)
  ):
  workspace_in_db = workspace.get_by_id(db, id=obj_id, user=current_user, req_type="read")
  dataset_ids = workspace_in_db.datasets["ids"]
  results = []
  for ds_id in dataset_ids:
    dataset_in_db = dataset.get_by_id(db=db, id=ds_id, user=current_user, req_type="read")
    results.append(dataset_in_db)
  return results


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


### work in progress
@router.post("/{obj_id}/comment",
  summary="Comment a workspace",
  description="Add a comment to a workspace",
  response_model=Comment
  )
async def comment_workspace(
  obj_id: int,
  obj_in: CommentWorkspace,
  background_tasks: BackgroundTasks,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user_optional)
  ):
  workspace_in_db = workspace.get_by_id(db=db, id=obj_id, user=current_user, req_type="comment")
  comment_in_db = comment.create(
    db=db,
    obj_in=obj_in,
  )
  return comment_in_db


### work in progress
@router.get("/{obj_id}/comments",
  summary="Get a workspace's comments",
  description="Get comments related to a workspace",
  response_model=List[Comment]
  )
async def get_comments_workspace(
  obj_id: int,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user_optional),
  skip: int = 0, limit: int = 100, 
  ):
  print("\nget_comments_workspace > obj_id : ", obj_id)
  # workspace_in_db = workspace.get_by_id(db=db, id=obj_id, user=current_user, req_type="read")
  comments_in_db = workspace.get_comments(
    db=db,
    id=obj_id,
    user=current_user,
    skip=skip,
    limit=limit,
  )
  print("get_comments_workspace > comments_in_db : ", comments_in_db)
  return comments_in_db


## work in progress
@router.post("/{obj_id}/patch",
  summary="Patch a workspace",
  description="Propose to patch a workspace",
  response_model=Patch
  )
async def patch_workspace(
  obj_id: int,
  obj_in: PatchWorkspace,
  background_tasks: BackgroundTasks,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user_optional)
  ):
  workspace_in_db = workspace.get_by_id(db=db, id=obj_id, user=current_user, req_type="patch")
  patch_in_db = patch.create(
    db=db,
    obj_in=obj_in,
  )
  return patch_in_db


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
