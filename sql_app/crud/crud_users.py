from . import (settings, Session, datetime, timedelta, 
  Optional, 
  HTTPException, status, Security, 
  Depends
)

from ..db.database import get_db
from ..security.jwt import ( 
  JWTError, jwt, CryptContext,
  OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes,
  SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES,
  pwd_context, oauth2_scheme
)

from ..models import models_user
from ..schemas import schemas_user, schemas_token


###  USER FIELDS ABLE TO BE UPDATED

FIELDS_UPDATE = [
  "name",
  "surname",
  "description",
  "avatar_url"
]

###  USER FUNCTIONS

def get_user_by_id(db: Session, user_id: int):
  return db.query(models_user.User).filter(models_user.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
  # print("get_user_by_email > email : ", email)
  return db.query(models_user.User).filter(models_user.User.email == email).first()


def update_user_field_in_db(
  db: Session,
  user_id: int,
  field: str,
  value: any
  ):
  print("update_user_in_db > field : ", field)
  print("update_user_in_db > value : ", value)
  if field not in FIELDS_UPDATE:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Field not open to update"
    )
  db_user = get_user_by_id(db=db, user_id=user_id)
  print("update_user_in_db > db_user : ", db_user)
  setattr(db_user, field, value)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user


def delete_user_in_db(
  db: Session,
  user_id: int, 
  current_user: schemas_user.User, 
  ):
  # query = users.delete().where(users.c.id == user.id)
  # await database.execute(query)
  # return user_id

  ### check if user has the right to delete another user or itself

  ### delete
  obj = db.query(models_user.User).get(user_id)
  db.delete(obj)
  db.commit()
  return obj


### AUTH FUNCTIONS

def create_access_token(
  data: dict,
  expires_delta: Optional[timedelta] = None
  ):
  to_encode = data.copy()
  print("create_access_token > to_encode : ", to_encode)
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt


async def get_current_user(
  security_scopes: SecurityScopes,
  db: Session = Depends(get_db),
  token: str = Depends(oauth2_scheme)
  ):
  print("get_current_user > security_scopes.scopes : ", security_scopes.scopes)
  if security_scopes.scopes:
    authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
  else:
    authenticate_value = f"Bearer"
  print("get_current_user > token : ", token)
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": authenticate_value}
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print("get_current_user > payload : ", payload)
    username: str = payload.get("sub")
    print("get_current_user > username : ", username)
    if username is None:
      raise credentials_exception
    token_scopes = payload.get("scopes", [])
    print("get_current_user > token_scopes : ", token_scopes)
    token_data = schemas_token.TokenData(scopes=token_scopes, username=username)
  except JWTError:
    raise credentials_exception
  user = get_user_by_email(db, email=token_data.username)
  if user is None:
    raise credentials_exception
  for scope in security_scopes.scopes:
    if scope not in token_data.scopes:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not enough permissions",
        headers={"WWW-Authenticate": authenticate_value},
      )
  return user


async def get_current_active_user(
  #current_user: schemas_user.User = Depends(get_current_user)
  current_user: schemas_user.User = Security(
    get_current_user,
    scopes=["me"]
    )
  ):
  print("get_current_active_user > current_user : ", current_user)
  if not current_user.is_active:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
  return current_user


def verify_password(plain_password, hashed_password):
  return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
  return pwd_context.hash(password)


def authenticate_user(db: Session, user_email: str, password: str):
  print("authenticate_user > user_email : ", user_email)
  user = get_user_by_email(db, user_email)
  print("authenticate_user > user : ", user)
  if not user:
    return False
  if not verify_password(password, user.hashed_password):
    return False
  return user


def create_user_in_db(db: Session, user: schemas_user.UserCreate):
  # print("create_user_in_db > user : ", user)
  db_user = models_user.User(email=user.email, username=user.username, hashed_password=get_password_hash(user.password))
  # print("create_user_in_db > db_user : ", db_user)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user



### USERS FUNCTIONS

def get_users(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models_user.User).offset(skip).limit(limit).all()

