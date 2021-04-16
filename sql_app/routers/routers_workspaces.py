from . import ( List, Session, APIRouter, Depends,
  HTTPException, status,
  get_db,
)

from ..schemas.schemas_workspace import Workspace, WorkspaceCreate, WorkspaceUpdate, WorkspaceList
from ..crud.crud_workspaces import workspace

from ..models.models_user import User
from ..crud.crud_users import (
  get_current_user,
)


router = APIRouter()


@router.post(
  "/",
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


@router.get(
  "/{obj_id}",
  summary="Get a workspace",
  description="Get a workspace by its id",
  response_model=WorkspaceList
  )
def read_workspace(obj_id: int , db: Session = Depends(get_db)):
  workspace_in_db = workspace.get_by_id(db, id=obj_id)
  if workspace_in_db is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workspace not found")
  return workspace_in_db


@router.get(
  "/",
  summary="Get a list of all workspaces",
  description="Get all workspaces given a limit",
  response_model=List[Workspace]
)
def read_workspaces(
  skip: int = 0, limit: int = 100, 
  db: Session = Depends(get_db)
  ):
  workspaces = workspace.get_multi(db, skip=skip, limit=limit)
  return workspaces
