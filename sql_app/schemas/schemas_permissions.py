from enum import Enum

class PermissionType(str, Enum):
  perm_owner = "owner-only"
  perm_groups = "owner+groups"
  perm_users = "owner+groups+users"
  perm_public = "public"
