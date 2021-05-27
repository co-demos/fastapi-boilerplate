from . import ( List, Session, APIRouter, Depends,
  HTTPException, status,
  get_db,
)

from fastapi.encoders import jsonable_encoder

from ..schemas.schemas_invitation import Invitation, InvitationCreate, InvitationUpdate, InvitationList
from ..crud.crud_invitations import invitation

from ..models.models_user import User
from ..crud.crud_users import user
from ..crud.crud_users import (
  get_current_user,
  get_current_active_user,
)

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
  response_model=Invitation,
  )
def read_invitation(
  obj_id: int, 
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  invitation_in_db = invitation.get_by_id(db, id=obj_id)
  if invitation_in_db is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invitation not found")
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
  invitation_in_db = invitation.get_by_id(db=db, id=obj_id)
  if invitation_in_db is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invitation not found")
  ### only owner and superuser for now
  ### need to check group and scope !!!
  if not current_user.is_superuser and (invitation_in_db.owner_id != current_user.id):
    raise HTTPException(status_code=400, detail="Not enough permissions")
  invitation_in_db = invitation.update(db=db, db_obj=invitation_in_db, obj_in=obj_in)
  return invitation_in_db


@router.get("/",
  summary="Get a list of all invitations",
  description="Get all invitations given a limit",
  response_model=List[Invitation]
)
def read_invitations(
  skip: int = 0, limit: int = 100, 
  current_user: User = Depends(get_current_user),
  db: Session = Depends(get_db),
  ):
  invitations = invitation.get_multi(db=db, skip=skip, limit=limit)
  return invitations


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
  print("delete_invitation > obj_id : ", obj_id)
  # invitation_in_db = invitation.get_by_id(db=db, id=id)
  # print("delete_invitation > invitation_in_db : ", invitation_in_db)
  # if not invitation_in_db:
  #   raise HTTPException(status_code=404, detail="invitation not found")
  invitation_deleted = invitation.remove(db=db, id=obj_id, current_user=current_user)
  print("delete_invitation > invitation_deleted : ", invitation_deleted)
  return invitation_deleted
