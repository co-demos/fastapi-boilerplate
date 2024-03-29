print(">>>>>> import routers.routers_invitations.py ...")

from . import ( List, Session, APIRouter, Depends,
  HTTPException, status, BackgroundTasks,
  get_db,
)

import datetime
from fastapi.encoders import jsonable_encoder

from ..schemas.schemas_invitation import Invitation, InvitationCreate, InvitationUpdate, InvitationsList, InvitationResponse
from ..schemas.schemas_choices import status_dict, invitee_id_dict
from ..crud.crud_invitations import invitation

from ..schemas.schemas_comment import Comment, CommentInvitation
from ..crud.crud_comments import comment

from ..models.models_user import User
from ..crud.crud_users import user
from ..crud.crud_users import (
  get_current_user,
  get_current_active_user,
)

from ..crud.crud_groups import group
from ..crud.crud_workspaces import workspace
from ..crud.crud_datasets import dataset
from ..crud.crud_tablemetas import tablemeta

crud_choices = {
  "group" : group,
  "workspace" : workspace,
  "dataset" : dataset,
  "tablemeta" : tablemeta,
}

from ..emails.emails import (
  send_invitation_email,
)

router = APIRouter()


@router.post("/",
  summary="Create an invitation",
  description="Create an invitation, including the id of the user creating the invitation",
  response_model=Invitation,
  status_code=status.HTTP_201_CREATED
  )
def create_invitation_for_user(
  obj_in: InvitationCreate,
  background_tasks: BackgroundTasks,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  user_id = current_user.id

  # send invitation email
  background_tasks.add_task(
    send_invitation_email,
    email_from=user_in.email,
    username=user_in.username,
    name=user_in.name,
    surname=user_in.surname,
    invitation=obj_in,
  )

  return invitation.create_with_owner(db=db, obj_in=obj_in, owner_id=user_id)


@router.get("/{obj_id}",
  summary="Get a invitation",
  description="Get a invitation by its id",
  # response_model=Invitation,
  )
def read_invitation(
  obj_id: int, 
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  # print("\nread_invitation > current_user.__dict__ : ", current_user.__dict__)
  print("\nread_invitation > current_user.email : ", current_user.email)
  print("read_invitation > current_user.id : ", current_user.id)
  # print("read_invitation > obj_id : ", obj_id)
  invitation_in_db = invitation.get_by_id(db, id=obj_id, user=current_user, req_type="read")

  print("read_invitation > invitation_in_db : ", invitation_in_db)
  print("read_invitation > invitation_in_db.owner_id : ", invitation_in_db.owner_id)
  print("read_invitation > invitation_in_db.owner : ", invitation_in_db.owner)

  invitation_model = Invitation.from_orm(invitation_in_db)
  invitation_dict = jsonable_encoder(invitation_model)
  # print("read_invitation > invitation_dict (simple): ", invitation_dict)

  item_type = invitation_in_db.invitation_to_item_type
  item_id = invitation_in_db.invitation_to_item_id
  item_crud = crud_choices[ item_type ]
  item_in_db = item_crud.get_by_id( db=db, id=item_id, user=current_user, req_type="read", get_auth_check=False )
  item_data = jsonable_encoder(item_in_db)

  invitation_dict["invitation_item"] = item_data
  # print("read_invitation > invitation_dict (extended): ", invitation_dict)

  # return invitation_in_db
  return invitation_dict


### work in progress
@router.post("/{obj_id}/comment",
  summary="Comment an invitation",
  description="Add a comment to an invitation",
  response_model=Comment
  )
async def comment_invitation(
  obj_id: int,
  obj_in: CommentInvitation,
  background_tasks: BackgroundTasks,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  invitation_in_db = invitation.get_by_id(db=db, id=obj_id, user=current_user, req_type="comment")
  comment_in_db = comment.create(
    db=db,
    obj_in=obj_in,
  )
  return comment_in_db

### work in progress
@router.get("/{obj_id}/comments",
  summary="Get a invitation's comments",
  description="Get comments related to a invitation",
  response_model=List[Comment]
  )
async def get_comments_invitation(
  obj_id: int,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user),
  skip: int = 0, limit: int = 100, 
  ):
  print("\nget_comments_invitation > obj_id : ", obj_id)
  comments_in_db = invitation.get_comments(
    db=db,
    id=obj_id,
    user=current_user,
    skip=skip,
    limit=limit,
  )
  print("get_comments_invitation > comments_in_db : ", comments_in_db)
  return comments_in_db


@router.post("/{obj_id}",
  summary="Accept / refuse a invitation",
  description="Accept / refuse a invitation by its id",
  response_model=Invitation
  )
async def respond_to_invitation(
  obj_id: int,
  obj_in: InvitationResponse,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  invitation_in_db = invitation.get_by_id(db=db, id=obj_id, user=current_user, req_type="response")
  
  print("\nrespond_to_invitation > obj_in : ", obj_in)
  print("respond_to_invitation > current_user.email : ", current_user.email)
  print("respond_to_invitation > invitation_in_db : ", invitation_in_db)
  invit_status = status_dict[obj_in.action]
  print("respond_to_invitation > invit_status : ", invit_status)

  ### update invitation
  invitation_in_db = invitation.update_status(db=db, db_obj=invitation_in_db, status=invit_status)
  invitation_data = jsonable_encoder(invitation_in_db)

  ### update target object
  item_type = invitation_in_db.invitation_to_item_type
  item_id = invitation_in_db.invitation_to_item_id
  invitee_type = invitation_in_db.invitee_type
  print("respond_to_invitation > item_type : ", item_type)
  print("respond_to_invitation > item_id : ", item_id)
  print("respond_to_invitation > invitee_type : ", invitee_type)
  
  item_crud = crud_choices[ item_type ]
  item_in_db = item_crud.get_by_id( db=db, id=item_id, user=current_user, req_type="read", get_auth_check=False )
  item_data = jsonable_encoder(item_in_db)
  print("respond_to_invitation > item_data : ", item_data )

  item_dict_fields = invitee_id_dict[invitee_type]
  invitee_id = invitation_data[ item_dict_fields["in_invit"] ]
  item_pending = item_data[ item_dict_fields["pending_field"] ]
  item_authorized = item_data[ item_dict_fields["authorized_field"] ]
  print("respond_to_invitation > item_pending : ", item_pending )
  print("respond_to_invitation > item_authorized : ", item_authorized )

  if item_pending and len(item_pending) :
    update_pending = [ i for i in item_pending if i[ item_dict_fields["in_item"] ] != invitee_id ]
    print("respond_to_invitation > update_pending : ", update_pending)
  else : 
    update_pending = []

  if item_authorized and len(item_authorized) :
    update_authorized = [ i for i in item_authorized if i[ item_dict_fields["in_item"] ] != invitee_id ]
  else :
    update_authorized = []

  if invit_status == "accepted" :
    time_accept = datetime.datetime.utcnow()
    new_authorized = {
      item_dict_fields["in_item"] : invitation_data[ item_dict_fields["in_invit"] ],
      'auths' : invitation_data["auths"],
      'invited_by' : invitation_data["owner_id"],
      'response_date' : time_accept.strftime(("Y-%m-%dT%H:%M:%S")),
    }
    print("respond_to_invitation > new_authorized : ", new_authorized)
    update_authorized.append(new_authorized)
    print("respond_to_invitation > update_authorized : ", update_authorized)

  update_data = {
    item_dict_fields["pending_field"]: update_pending,
    item_dict_fields["authorized_field"]: update_authorized,
  }
  print("\nrespond_to_invitation > update_data : ", update_data)

  item_in_db = item_crud.update(db=db, db_obj=item_in_db, obj_in=update_data)

  return invitation_in_db


@router.put("/{obj_id}",
  summary="Update a invitation",
  description="Update a invitation by its id",
  response_model=Invitation
  )
def update_invitation(
  obj_id: int,
  obj_in: InvitationUpdate,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  invitation_in_db = invitation.get_by_id(db=db, id=obj_id, user=current_user, req_type="write")
  invitation_in_db = invitation.update(db=db, db_obj=invitation_in_db, obj_in=obj_in)
  return invitation_in_db


# @router.get("/",
#   summary="Get a list of all invitations",
#   description="Get all invitations given a limit",
#   response_model=List[Invitation]
# )
# def read_invitations(
#   skip: int = 0, limit: int = 100, 
#   current_user: User = Depends(get_current_user),
#   db: Session = Depends(get_db),
#   ):
#   invitations = invitation.get_multi(db=db, skip=skip, limit=limit, user=current_user, req_type="read")
#   return invitations


@router.delete("/{obj_id}",
  summary="Delete a invitation",
  description="Delete a invitation by its id",
  response_model=Invitation
  )
def delete_invitation(
  obj_id: int,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  print("\ndelete_invitation > obj_id : ", obj_id)
  print("delete_invitation > current_user.email : ", current_user.email)
  
  invitation_in_db = invitation.get_by_id(db=db, id=obj_id, user=current_user, req_type="manage")
  print("delete_invitation > invitation_in_db : ", invitation_in_db)

  invitation_data = jsonable_encoder(invitation_in_db)
  print("delete_invitation > invitation_data : ", invitation_data)

  ### update target object
  item_type = invitation_in_db.invitation_to_item_type
  item_id = invitation_in_db.invitation_to_item_id
  invitee_type = invitation_in_db.invitee_type
  print("delete_invitation > item_type : ", item_type)
  print("delete_invitation > item_id : ", item_id)
  print("delete_invitation > invitee_type : ", invitee_type)

  item_crud = crud_choices[ item_type ]
  item_in_db = item_crud.get_by_id( db=db, id=item_id, user=current_user, req_type="manage" )
  item_data = jsonable_encoder(item_in_db)
  print("delete_invitation > item_data : ", item_data )

  item_dict_fields = invitee_id_dict[invitee_type]
  invitee_id = invitation_data[ item_dict_fields["in_invit"] ]
  item_pending = item_data[ item_dict_fields["pending_field"] ]
  item_authorized = item_data[ item_dict_fields["authorized_field"] ]
  print("delete_invitation > item_pending : ", item_pending )
  print("delete_invitation > item_authorized : ", item_authorized )

  ### delete invitee from pending_users
  if item_pending and len(item_pending) :
    update_pending = [ i for i in item_pending if i[ item_dict_fields["in_item"] ] != invitee_id ]
    print("delete_invitation > update_pending : ", update_pending)
  else : 
    update_pending = []

  update_data = {
    item_dict_fields["pending_field"]: update_pending,
  }
  print("\nrespond_to_invitation > update_data : ", update_data)

  item_in_db = item_crud.update(db=db, db_obj=item_in_db, obj_in=update_data)
  
  ### delete invit for good
  invitation_deleted = invitation.remove(db=db, id=obj_id, current_user=current_user)
  print("delete_invitation > invitation_deleted : ", invitation_deleted)
  return invitation_deleted
  # return invitation_in_db
