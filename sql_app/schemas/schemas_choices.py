print(">>>>>> import schemas_choices.py >  PermissionType ...")
from enum import Enum

class PermissionType(str, Enum):
  perm_owner = "owner-only"
  perm_groups = "owner+groups"
  perm_users = "owner+groups+users"
  perm_public = "public"


class InviteeType(str, Enum):
  user = "user"
  group = "group"


class ItemType(str, Enum):
  user = "user"
  group = "group"
  workspace = "workspace"
  dataset = "dataset"
  table = "table"


class ItemTypeExtended(str, Enum):
  user = "user"
  group = "group"
  workspace = "workspace"
  dataset = "dataset"
  table = "table"
  invitation = "invitation"
  message = "message"
  comment = "comment"
  moderation = "moderation"


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


class InvitationStatusAction(str, Enum):
  accept = "accept"
  refuse = "refuse"


class EmitAction(str, Enum):
  add = "add"
  join = "join"
  comment = "comment"
  edit = "edit"
  invite = "invite"
  delete = "delete"
  accept = "accept"
  refuse = "refuse"


status_dict = {
  "accept": "accepted",
  "refuse": "refused",
}

# pending_dict = {
#   "group": "pending_groups",
#   "user": "pending_users",
# }
# authorized_dict = {
#   "group": "authorized_groups",
#   "user": "authorized_users",
# }
invitee_id_dict = {
  "group": {
    "in_invit": "invitee_id",
    "in_item": "group_id",
    "pending_field": "pending_groups",
    "authorized_field": "authorized_groups"
  },
  "user": {
    "in_invit": "invitee",
    "in_item": "user_email",
    "pending_field": "pending_users",
    "authorized_field": "authorized_users" 
  },
}
