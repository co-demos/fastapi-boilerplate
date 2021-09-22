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
  item = "item"


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
  read = "read"
  like = "like"


class CallbackMethod(str, Enum):
  get = "get"
  put = "put"
  post = "post"
  delete = "delete"


class RequestType(str, Enum):
  read = "read"
  comment = "comment"
  patch = "patch"
  write = "write"
  manage = "manage"


class ListTypes(str, Enum):
  user = "user"
  shared = "shared"
  mix = "mix"

  # get_item = "get_item"
  # get_invitations = "get_invitations"
  # get_workspaces = "get_workspaces"
  # get_datasets = "get_datasets"
  # get_tablemetas = "get_tablemetas"
  # get_groups = "get_groups"
  # get_messages = "get_messages"

  # append_item = "append_item"
  # append_invitation = "append_invitation"
  # append_workspace = "append_workspace"
  # append_dataset = "append_dataset"
  # append_tablemeta = "append_tablemeta"
  # append_group = "append_group"
  # append_message = "append_message"

status_dict = {
  "accept": "accepted",
  "refuse": "refused",
}

messages_dict = {
  "accept": "accepted your",
  "refuse": "refused your",
  "add": "added you to",
  "join": "joined you on",
  "comment": "commented your",
  "edit": "edited your",
  "invite": "invited you to",
  "remove": "removed your",
  "delete": "deleted your",
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
