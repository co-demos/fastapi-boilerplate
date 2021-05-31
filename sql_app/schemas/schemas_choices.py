print(">>>>>> import schemas_choices.py >  PermissionType ...")
from enum import Enum

class PermissionType(str, Enum):
  perm_owner = "owner-only"
  perm_groups = "owner+groups"
  perm_users = "owner+groups+users"
  perm_public = "public"


class ItemType(str, Enum):
  user = "user"
  group = "group"
  workspace = "workspace"
  dataset = "dataset"
  table = "table"


class ItemTypes(str, Enum):
  users = "users"
  groups = "groups"
  workspaces = "workspaces"
  datasets = "datasets"
  tables = "tables"


class InvitationStatus(str, Enum):
  pending = "pending"
  accepted = "accepted"
  refused = "refused"


class OperatorType(str, Enum):
  or_ = "or"
  and_ = "and"
  not_ = "not"
