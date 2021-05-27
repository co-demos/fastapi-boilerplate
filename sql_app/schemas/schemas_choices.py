print(">>>>>> import schemas_choices.py >  PermissionType ...")
from enum import Enum

class PermissionType(str, Enum):
  perm_owner = "owner-only"
  perm_groups = "owner+groups"
  perm_users = "owner+groups+users"
  perm_public = "public"


class ItemType(str, Enum):
  workspace = "workspace"
  dataset = "dataset"
  table = "table"
  group = "group"


class InvitationStatus(str, Enum):
  pending = "pending"
  accepted = "accepted"
  refused = "refused"
