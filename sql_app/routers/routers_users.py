print(">>>>>> import routers.routers_user.py ...")

from pydantic.networks import EmailStr

from . import ( settings,
  List, Session, APIRouter, Depends, Body, 
  BackgroundTasks, Security,
  HTTPException, status, 
  timedelta,
  File, UploadFile, shutil,
  jsonable_encoder,
  get_db, Query,

  # crud_items,
  crud_posts,
  crud_comments,
)

from ..schemas.schemas_item import Item, ItemCreate
from ..schemas.schemas_post import Post
from ..schemas.schemas_comment import Comment

from ..schemas.schemas_invitation import Invitation, InvitationBasics

from ..models.models_user import User as UserModel
from ..schemas.schemas_user import User, UserInfos, UserCreate, UserUpdate, UserBasicInfos, UserUX
from ..schemas.schemas_token import TokenAccess, TokenAccessRefresh
from ..schemas.schemas_message import Msg

from ..crud.crud_users import user, get_current_active_user, get_current_active_user_refresh, get_password_hash
from ..crud.crud_invitations import invitation

from ..security.jwt import ( JWTError, jwt, CryptContext, 
  OAuth2PasswordBearer, OAuth2PasswordRequestForm,
  SECRET_KEY, ALGORITHM, 
  ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES,
  pwd_context, oauth2_scheme,
  create_access_token, verify_password_reset_token, generate_password_reset_token, 
)

from .routers_invitations import read_invitation


from ..emails.emails import (
  send_test_email,
  send_new_account_email,
  send_reset_password_email
)


router = APIRouter()



### USER FUNCTIONS

@router.post("/",
  summary="Create an user",
  response_model=User,
  status_code=status.HTTP_201_CREATED
  )
def create_user(
  user_in: UserCreate, 
  background_tasks: BackgroundTasks,
  db: Session = Depends(get_db),
  ):
  """
  Create an user with basic information:

  - **email**: the email is necessary and is used as primary identifier
  - **username**: choose a pseudo
  - **password**: a password chosen by the user
  """
  print("create_user > user_in : ", user_in)

  # user_in_db = get_user_by_email(db, email=user_in.email)
  user_in_db = user.get_user_by_email(db, email=user_in.email)
  if user_in_db:
    raise HTTPException(status_code=400, detail="Email already registered")
  if settings.EMAILS_ENABLED and user_in.email:
    email_verify_token = generate_password_reset_token(email=user_in.email)

    background_tasks.add_task(
      send_new_account_email,
      email_to=user_in.email,
      name=user_in.name,
      surname=user_in.surname,
      username=user_in.username,
      password=user_in.password,
      token=email_verify_token
    )

  return user.create_user_in_db(db=db, user_in=user_in)


@router.get("/",
  summary="Get a list of users",
  description="Get a list of all users given a limit",
  response_model=List[User]
  )
def read_users(
  skip: int = 0,
  limit: int = 100, 
  db: Session = Depends(get_db)
  ):
  users_in_db = user.get_multi(db, skip=skip, limit=limit)
  return users_in_db


@router.get("/{user_id}",
  summary="Get an user",
  description="Get infos of one user",
  response_model=User
 )
def read_user(
  user_id: int,
  db: Session = Depends(get_db)
  ):
  user_in_db = user.get_by_id(db, id=user_id)
  if user_in_db is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="User not found"
    )
  user_dict = jsonable_encoder(user_in_db)
  print("read_user > user_dict : ", user_dict)
  return user_in_db


@router.delete("/{user_id}",
  summary="Delete an user",
  description="Detete infos of one user",
  )
def delete_user(
  user_id: int, 
  db: Session = Depends(get_db),
  current_user: UserModel = Depends(get_current_active_user)
  ):
  user_deleted = user.remove_user(db=db, id=user_id, current_user=current_user)
  return {
    "status" : True,
    "user_deleted_id": user_deleted.id,
    "user_deleted_email": user_deleted.email,
    "message": "This user has been deleted successfully." 
  }


# @router.post("/{user_id}/items/",
#   summary="Create an item for any user",
#   description="Create an item to another user given the user id",
#   response_model=Item,
#   status_code=status.HTTP_201_CREATED
# )
# def create_item_for_user(
#   user_id: int, 
#   item: ItemCreate,
#   db: Session = Depends(get_db)
#   ):
#   return crud_items.create_user_item(db=db, item=item, user_id=user_id)



### ME ROUTES

@router.get("/me/",
  summary="Get infos for connected/authenticated user",
  description="Get infos for connected/authenticated user",
  response_model=User
  )
async def read_users_me(
  current_user: UserModel = Depends(get_current_active_user)
  ):
  print("\n read_users_me > current_user.__dict__ : ", current_user.__dict__)
  return current_user


@router.put("/me/",
  summary="Update user",
  description="Update user",
  response_model=User
  )
async def update_user(
  user_in: UserBasicInfos,
  current_user: UserModel = Depends(get_current_active_user),
  db: Session = Depends(get_db)
  ):
  print("\nupdate_user > user_in : ", user_in)
  
  current_user_data = jsonable_encoder(current_user)
  print("update_user > current_user_data : ", current_user_data)
  
  user_in_db = user.update(db, db_obj=current_user, obj_in=user_in)
  print("update_user > user_in_db : ", user_in_db)
  return user_in_db


@router.get("/me/ux",
  summary="Get user ux",
  description="Get user ux preferences",
  response_model=UserUX
  )
async def read_user_ux(
  current_user: UserModel = Depends(get_current_active_user),
  db: Session = Depends(get_db)
  ):
  current_user_data = jsonable_encoder(current_user)
  print("read_user_ux > current_user_data : ", current_user_data)
  return current_user_data


@router.put("/me/ux",
  summary="Update user ux",
  description="Update user ux",
  response_model=UserUX
  )
async def update_user_ux(
  ux_in: UserUX,
  current_user: UserModel = Depends(get_current_active_user),
  db: Session = Depends(get_db)
  ):
  print("\nupdate_user_ux > ux_in : ", ux_in)
  
  current_user_data = jsonable_encoder(current_user)
  print("update_user_ux > current_user_data : ", current_user_data)
  
  user_in_db = user.update(db, db_obj=current_user, obj_in=ux_in)
  print("update_user_ux > jsonable_encoder(user_in_db) : ", jsonable_encoder(user_in_db))
  return jsonable_encoder(user_in_db)


@router.patch("/me/update_avatar",
  summary="Update user avatar",
  description="Update user avatar by uploading a file",
  response_model=User
  )
async def update_user_avatar(
  uploaded_file: UploadFile = File(...),
  current_user: UserModel = Depends(get_current_active_user),
  db: Session = Depends(get_db)
  ):
  user_id = current_user.id
  with open ("media/"+uploaded_file.filename, "wb+") as file_object:
    shutil.copyfileobj(uploaded_file.file, file_object)
  field = "avatar_url"
  url = str("media/"+uploaded_file.filename)
  # return update_user_field_in_db(db=db, user_id=user_id, field=field, value=url)
  return user.update(db=db, user_id=user_id, field=field, value=url)


# @router.get("/me/items/",
#   summary="Get user's own items",
#   description="Get connected/authenticated user's own items",
# )
# async def read_own_items(
#   current_user: UserModel = Depends(get_current_active_user),
#   db: Session = Depends(get_db)
#   ):
#   user_id = current_user.id
#   user_items = crud_items.get_user_items(db=db, user_id=user_id)
#   return [{"items": user_items, "owner": current_user.email, "owner_id": current_user.id}]


@router.get("/me/posts/",
  summary="Get user's own posts",
  description="Get connected/authenticated user's own posts",
 )
async def read_own_posts(
  current_user: UserModel = Depends(get_current_active_user),
  db: Session = Depends(get_db)
  ):
  user_id = current_user.id
  user_posts = crud_posts.get_user_posts(db=db, user_id=user_id)
  return [{"posts": user_posts, "owner": current_user.email, "owner_id": current_user.id}]


@router.get("/me/invitations/",
  summary="Get user's own invitations",
  description="Get connected/authenticated user's own invitations",
 )
async def read_own_invitations(
  current_user: UserModel = Depends(get_current_active_user),
  db: Session = Depends(get_db)
  ):
  # print("read_own_invitations > current_user : ", current_user)
  user_id = current_user.id
  user_email = current_user.email
  # print("read_own_invitations > user_id : ", user_id)
  # print("read_own_invitations > user_email : ", user_email)

  user_invits_sent = invitation.get_multi_by_owner(db=db, owner_id=user_id, limit=None)
  # print("read_own_invitations > user_invits_sent : ", user_invits_sent)
  # user_invits_sent_extended = [ Invitation.from_orm(invit) for invit in user_invits_sent ]
  user_invits_sent_extended = [ read_invitation(obj_id=invit.id, db=db, current_user=current_user ) for invit in user_invits_sent ]
  # print("read_own_invitations > user_invits_sent_extended : ", user_invits_sent_extended)

  user_invits_received = invitation.get_multi_received(db=db, user_email=user_email, limit=None)
  # print("read_own_invitations > user_invits_received : ", user_invits_received)
  # user_invits_received_extended = [ Invitation.from_orm(invit) for invit in user_invits_received ]
  user_invits_received_extended = [ read_invitation(obj_id=invit.id, db=db, current_user=current_user ) for invit in user_invits_received ]
  # print("read_own_invitations > user_invits_received_extended : ", user_invits_received_extended)

  # return {
  #   "invitations_sent": user_invits_sent_extended,
  #   "invitations_received": user_invits_received_extended,
  # }

  return user_invits_sent_extended + user_invits_received_extended


@router.get("/me/comments/",
  summary="Get user's own comments",
  description="Get connected/authenticated user's own comments",
  )
async def read_own_comments(
  current_user: UserModel = Depends(get_current_active_user),
  db: Session = Depends(get_db)
  ):
  user_id = current_user.id
  user_comments = crud_comments.get_user_comments(db=db, user_id=user_id)
  return [{"comments": user_comments, "owner": current_user.email, "owner_id": current_user.id}]


### AUTH ROUTES

@router.post("/token",
  summary="Create an access token for login",
  response_model=TokenAccessRefresh,
  status_code=status.HTTP_201_CREATED
  )
async def login_for_access_token(
  db: Session = Depends(get_db),
  form_data: OAuth2PasswordRequestForm = Depends()
  ):
  """
  Create an access token according to Oauth2 specs.
  The request must be sent by form data. This form must have the following fields : 

  - **userrname**: here enter the user's email
  - **password**: the user's password
  """
  # print("login_for_access_token > form_data : ", form_data)
  # print("login_for_access_token > form_data.username : ", form_data.username)
  # print("login_for_access_token > form_data.password : ", form_data.password)
  # print("login_for_access_token > form_data.scopes : ", form_data.scopes)
  user_in_db = user.authenticate_user(db, form_data.username, form_data.password)
  if not user_in_db:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect username or password",
      headers={"WWW-Authenticate": "Bearer"},
    )
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
  # print("login_for_access_token > user_in_db : ", user_in_db)
  # print("login_for_access_token > form_data.scopes : ", form_data.scopes)
  # print("login_for_access_token > form_data.username : ", form_data.username)
  access_token = create_access_token(
    data={
      "sub": user_in_db.email, 
      "scopes": form_data.scopes
    },
    expires_delta=access_token_expires
  )
  refresh_token = create_access_token(
    data={
      "sub": user_in_db.email,
      "scopes": ["refresh"]
    },
    expires_delta=refresh_token_expires
  )
  return {
    "refresh_token": refresh_token, 
    "access_token": access_token, 
    "token_type": "bearer"
  }


@router.get("/verify-acces-token/",
  summary="Verify user's access token",
  description="Verify user's access token",
  response_model=Msg
  )
async def verify_access_token(
  current_user: UserModel = Depends(get_current_active_user)
  ):
  return { "msg": "Access token is stil valid"}


@router.get("/new-access-token/",
  summary="New access token from refresh token validation",
  description="New access token from refresh token validation",
  response_model=TokenAccess
  )
async def new_access_token(
  current_user: UserModel = Depends(get_current_active_user_refresh)
  ):
  print("new_access_token > current_user : ", current_user)
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(
    data={
      "sub": current_user.email,
      "scopes": ["me"]
    },
    expires_delta=access_token_expires
  )
  return {
    "access_token": access_token, 
    "token_type": "bearer"
  }


### PASSWORD RECOVERY

# @router.post("/test-email/",
#   response_model=Msg,
#   status_code=201
# )
# def test_email(
  #   email_to: EmailStr,
  #   # current_user: UserModel = Depends(get_current_active_superuser),
  #   current_user: UserModel = Depends(get_current_active_user),
  # ) :
  # """
  # Test emails.
  # """
  # send_test_email(email_to=email_to)
  # return {"msg": "Test email sent"}


@router.post("/password-recovery/{email}",
  response_model=Msg
 )
def password_recovery(
  email: str,
  background_tasks: BackgroundTasks,
  db: Session = Depends(get_db)
  ):
  """
  Password Recovery
  """
  user_in_db = user.get_user_by_email(db, email=email)
  print("password_recovery > user_in_db : ", user_in_db)
  if not user_in_db:
    raise HTTPException(
      status_code=404,
      detail="The user with this email does not exist in the system.",
    )
  password_reset_token = generate_password_reset_token(email=user_in_db.email)
  # send_reset_password_email(
  #   email_to=user_in_db.email,
  #   user=user_in_db,
  #   token=password_reset_token
  # )
  background_tasks.add_task(
    send_reset_password_email,
    email_to=user_in_db.email,
    user=user_in_db,
    token=password_reset_token
  )
  return {"msg": f"Password recovery email sent to {user_in_db.email}"}


@router.post("/reset-password/",
  response_model=Msg
  )
def reset_password(
  token: str = Body(...),
  new_password: str = Body(...),
  db: Session = Depends(get_db),
  ):
  """
  Reset password
  """
  print("reset_password > token : ", token)
  print("reset_password > new_password : ", new_password)
  email = verify_password_reset_token(token)
  print("reset_password > email : ", email)
  if not email:
    raise HTTPException(status_code=400, detail="Invalid token")
  user_in_db = user.get_user_by_email(db, email=email)
  if not user_in_db:
    raise HTTPException(
      status_code=404,
      detail="The user with this email does not exist in the system.",
    )
  elif not user_in_db.is_active:
    raise HTTPException(
      status_code=400,
      detail="Inactive user"
  )
  hashed_password = get_password_hash(new_password)
  user_in_db.hashed_password = hashed_password
  db.add(user_in_db)
  db.commit()
  return {"msg": f"Password updated successfully for user {user_in_db.email}"}


@router.get("/verify-email/",
  response_model=Msg
  )
def verify_email(
  token: str,
  db: Session = Depends(get_db),
  ):
  """
  Verify email
  """
  print("verify_email > token : ", token)
  email = verify_password_reset_token(token)
  print("verify_email > email : ", email)
  if not email:
    raise HTTPException(status_code=400, detail="Invalid token")
  user_in_db = user.get_user_by_email(db, email=email)
  print("verify_email > user_in_db : ", user_in_db)
  if not user_in_db:
    raise HTTPException(
      status_code=404,
      detail="The user with this email does not exist in the system.",
    )
  elif user_in_db.is_active:
    raise HTTPException(
      status_code=400,
      detail="User is already verified and active"
  )
  user_in_db.is_active = True
  db.add(user_in_db)
  db.commit()
  return {"msg": f"Email {email} was verified and user is now active !"}
