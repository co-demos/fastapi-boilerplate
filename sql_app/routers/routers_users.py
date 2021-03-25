import os

from . import ( List, Session, APIRouter, Depends, 
  HTTPException, status, timedelta,
  File, UploadFile,
  get_db,
  schemas_user, crud_users, models_user,
  schemas_item, crud_items,
  schemas_post, crud_posts,
  schemas_token
)

from ..security.jwt import ( JWTError, jwt, CryptContext, 
  OAuth2PasswordBearer, OAuth2PasswordRequestForm,
  SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, 
  pwd_context, oauth2_scheme
)

from ..crud.crud_users import ( authenticate_user, create_access_token,
  create_user_in_db,
  get_user_by_email, get_user_by_id, get_current_user, get_current_active_user,
  get_users
)

router = APIRouter()


### USER FUNCTIONS

@router.post("/", response_model=schemas_user.User)
def create_user(
  user: schemas_user.UserCreate, 
  db: Session = Depends(get_db)
  ):
  db_user = get_user_by_email(db, email=user.email)
  if db_user:
    raise HTTPException(status_code=400, detail="Email already registered")
  return create_user_in_db(db=db, user=user)


@router.get("/", response_model=List[schemas_user.User])
def read_users(
  skip: int = 0, limit: int = 100, 
  db: Session = Depends(get_db)
  ):
  users = get_users(db, skip=skip, limit=limit)
  return users


@router.get("/{user_id}", response_model=schemas_user.User)
def read_user(
  user_id: int,
  db: Session = Depends(get_db)
  ):
  db_user = get_user_by_id(db, user_id=user_id)
  if db_user is None:
    raise HTTPException(status_code=404, detail="User not found")
  return db_user


@router.post("/{user_id}/items/", response_model=schemas_item.Item)
def create_item_for_user(
  user_id: int, 
  item: schemas_item.ItemCreate,
  db: Session = Depends(get_db)
):
  return crud_items.create_user_item(db=db, item=item, user_id=user_id)


@router.get("/me/", response_model=schemas_user.User)
async def read_users_me(
  current_user: models_user.User = Depends(get_current_active_user)
  ):
  return current_user


@router.get("/me/items/")
async def read_own_items(
  current_user: models_user.User = Depends(get_current_active_user),
  db: Session = Depends(get_db)
  ):
  user_id = current_user.id
  user_items = crud_items.get_user_items(db=db, user_id=user_id)
  return [{"items": user_items, "owner": current_user.email, "owner_id": current_user.id}]

@router.get("/me/posts/")
async def read_own_posts(
  current_user: models_user.User = Depends(get_current_active_user),
  db: Session = Depends(get_db)
  ):
  user_id = current_user.id
  user_posts = crud_posts.get_user_posts(db=db, user_id=user_id)
  return [{"posts": user_posts, "owner": current_user.email, "owner_id": current_user.id}]


### AUTH ROUTES

@router.post("/token", response_model=schemas_token.Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
  print("login_for_access_token > form_data : ", form_data)
  user = authenticate_user(db, form_data.username, form_data.password)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect username or password",
      headers={"WWW-Authenticate": "Bearer"},
    )
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  print("login_for_access_token > user : ", user)
  print("login_for_access_token > form_data.scopes : ", form_data.scopes)
  print("login_for_access_token > form_data.username : ", form_data.username)
  access_token = create_access_token(
    # data={"sub": user.username},
    data={"sub": user.email, "scopes": form_data.scopes},
    expires_delta=access_token_expires
  )
  return {"access_token": access_token, "token_type": "bearer"}

