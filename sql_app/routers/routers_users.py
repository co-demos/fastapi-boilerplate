import os

from . import ( List, Session, APIRouter, Depends, 
  HTTPException, status, 
  timedelta,
  File, UploadFile, shutil,
  get_db,
  schemas_item, crud_items,
  schemas_post, crud_posts,
  schemas_comment, crud_comments,
  schemas_user, crud_users, models_user,
  schemas_token
)

from ..security.jwt import ( JWTError, jwt, CryptContext, 
  OAuth2PasswordBearer, OAuth2PasswordRequestForm,
  SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, 
  pwd_context, oauth2_scheme
)

from ..crud.crud_users import ( authenticate_user, create_access_token,
  create_user_in_db, update_user_field_in_db,
  get_user_by_email, get_user_by_id, get_current_user, get_current_active_user,
  get_users
)


router = APIRouter()


### USER FUNCTIONS

@router.post(
  "/",
  summary="Create an user",
  response_model=schemas_user.User,
  status_code=status.HTTP_201_CREATED
)
def create_user(
  user: schemas_user.UserCreate, 
  db: Session = Depends(get_db)
  ):
  """
  Create an user with basic information:

  - **email**: the email is necessary and is used as primary identifier
  - **username**: choose a pseudo
  - **password**: a password chosen by the user
  """
  db_user = get_user_by_email(db, email=user.email)
  if db_user:
    raise HTTPException(status_code=400, detail="Email already registered")
  return create_user_in_db(db=db, user=user)


@router.get(
  "/",
  summary="Get a list of users",
  description="Get a list of all users given a limit",
  response_model=List[schemas_user.User]
)
def read_users(
  skip: int = 0, limit: int = 100, 
  db: Session = Depends(get_db)
  ):
  users = get_users(db, skip=skip, limit=limit)
  return users


@router.get(
  "/{user_id}",
  summary="Get an user",
  description="Get infos of one user",
  response_model=schemas_user.User
)
def read_user(
  user_id: int,
  db: Session = Depends(get_db)
  ):
  db_user = get_user_by_id(db, user_id=user_id)
  if db_user is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
  return db_user


@router.delete(
  "/{user_id}",
  summary="Delete an user",
  description="Detete infos of one user",
)
def delete_user(
  user_id: int, 
  db: Session = Depends(get_db),
  current_user: models_user.User = Depends(get_current_active_user)
  ):
  user_deleted_id = crud_users.delete_user_in_db(db=db, user_id=user_id, current_user=current_user)
  return {
    "status" : True,
    "user_deleted_id": user_deleted_id,
    "message": "This user has been deleted successfully." 
  }

@router.post(
  "/{user_id}/items/",
  summary="Create an item for any user",
  description="Create an item to another user given the user id",
  response_model=schemas_item.Item,
  status_code=status.HTTP_201_CREATED
)
def create_item_for_user(
  user_id: int, 
  item: schemas_item.ItemCreate,
  db: Session = Depends(get_db)
  ):
  return crud_items.create_user_item(db=db, item=item, user_id=user_id)



### ME ROUTES

@router.get(
  "/me/",
  summary="Get infos for connected/authenticated user",
  description="Get infos for connected/authenticated user",
  response_model=schemas_user.User
)
async def read_users_me(
  current_user: models_user.User = Depends(get_current_active_user)
  ):
  return current_user


@router.patch(
  "/me/update_avatar",
  summary="Update user avatar",
  description="Update user avatar by uploading a file",
  response_model=schemas_user.User
)
async def update_user_avatar(
  uploaded_file: UploadFile = File(...),
  current_user: models_user.User = Depends(get_current_active_user),
  db: Session = Depends(get_db)
  ):
  user_id = current_user.id
  with open ("media/"+uploaded_file.filename, "wb+") as file_object:
    shutil.copyfileobj(uploaded_file.file, file_object)
  field = "avatar_url"
  url = str("media/"+uploaded_file.filename)
  return update_user_field_in_db(db=db, user_id=user_id, field=field, value=url)


@router.get(
  "/me/items/",
  summary="Get user's own items",
  description="Get connected/authenticated user's own items",
)
async def read_own_items(
  current_user: models_user.User = Depends(get_current_active_user),
  db: Session = Depends(get_db)
  ):
  user_id = current_user.id
  user_items = crud_items.get_user_items(db=db, user_id=user_id)
  return [{"items": user_items, "owner": current_user.email, "owner_id": current_user.id}]


@router.get(
  "/me/posts/",
  summary="Get user's own posts",
  description="Get connected/authenticated user's own posts",
)
async def read_own_posts(
  current_user: models_user.User = Depends(get_current_active_user),
  db: Session = Depends(get_db)
  ):
  user_id = current_user.id
  user_posts = crud_posts.get_user_posts(db=db, user_id=user_id)
  return [{"posts": user_posts, "owner": current_user.email, "owner_id": current_user.id}]


@router.get(
  "/me/comments/",
  summary="Get user's own comments",
  description="Get connected/authenticated user's own comments",
)
async def read_own_comments(
  current_user: models_user.User = Depends(get_current_active_user),
  db: Session = Depends(get_db)
  ):
  user_id = current_user.id
  user_comments = crud_comments.get_user_comments(db=db, user_id=user_id)
  return [{"comments": user_comments, "owner": current_user.email, "owner_id": current_user.id}]


### AUTH ROUTES

@router.post(
  "/token",
  summary="Create an access token for login",
  response_model=schemas_token.Token,
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
  user = authenticate_user(db, form_data.username, form_data.password)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect username or password",
      headers={"WWW-Authenticate": "Bearer"},
    )
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  # print("login_for_access_token > user : ", user)
  # print("login_for_access_token > form_data.scopes : ", form_data.scopes)
  # print("login_for_access_token > form_data.username : ", form_data.username)
  access_token = create_access_token(
    # data={"sub": user.username},
    data={"sub": user.email, "scopes": form_data.scopes},
    expires_delta=access_token_expires
  )
  return {"access_token": access_token, "token_type": "bearer"}

