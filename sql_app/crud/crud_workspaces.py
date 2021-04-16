from . import (pp, Session)

from ..db.database import get_db

from .base import CRUDBase
from ..models.models_workspace import Workspace
from ..schemas.schemas_workspace import WorkspaceCreate, WorkspaceUpdate


class CRUDWorkspace(CRUDBase[Workspace, WorkspaceCreate, WorkspaceUpdate]):
  pass

workspace = CRUDWorkspace(Workspace)


