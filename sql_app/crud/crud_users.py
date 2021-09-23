from . import (pp, settings, Session, datetime, timedelta, 
  Optional, 
  HTTPException, status, Security,
  Depends
)

from ..db.database import get_db
from ..security.jwt import ( 
  JWTError, jwt, CryptContext,
  OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes,
  SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES,
  pwd_context, oauth2_scheme, oauth2_scheme_optional
)

from .base import CRUDBase
from ..models.models_user import User

from ..schemas.schemas_user import UserCreate, UserUpdate
from ..schemas.schemas_token import TokenData


###  USER FIELDS ABLE TO BE UPDATED

FIELDS_UPDATE = [
  "name",
  "surname",
  "description",
  "avatar_url",
  # "read"
  # "comment"
]


### AUTH FUNCTIONS


def verify_password(plain_password, hashed_password):
  print("authenticate_user > plain_password : ", plain_password)
  print("authenticate_user > hashed_password : ", hashed_password)
  return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
  return pwd_context.hash(password)



def get_user_from_token(
  security_scopes = None,
  db: Session = Depends(get_db),
  token: str = None
  ):

  if security_scopes and security_scopes.scopes:
    authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
  else:
    authenticate_value = f"Bearer"
  print("get_user_from_token > token : ", token)
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": authenticate_value}
  )

  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print("get_user_from_token > payload : ", payload)
    username: str = payload.get("sub")
    print("get_user_from_token > username : ", username)
    if username is None:
      raise credentials_exception
    token_scopes = payload.get("scopes", [])
    print("get_user_from_token > token_scopes : ", token_scopes)
    token_data = TokenData(scopes=token_scopes, username=username)
  except JWTError:
    raise credentials_exception
  
  user_in_db = user.get_user_by_email(db, email=token_data.username)
  if user is None:
    raise credentials_exception
  for scope in security_scopes.scopes:
    if scope not in token_data.scopes:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not enough permissions",
        headers={"WWW-Authenticate": authenticate_value},
      )

  print("\n")
  return user_in_db  


async def get_current_user(
  security_scopes: SecurityScopes,
  db: Session = Depends(get_db),
  token: str = Depends(oauth2_scheme)
  ):
  print("\nget_current_user > security_scopes.scopes : ", security_scopes.scopes)
  
  # if security_scopes.scopes:
  #   authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
  # else:
  #   authenticate_value = f"Bearer"
  # print("get_current_user > token : ", token)
  # credentials_exception = HTTPException(
  #   status_code=status.HTTP_401_UNAUTHORIZED,
  #   detail="Could not validate credentials",
  #   headers={"WWW-Authenticate": authenticate_value}
  # )

  user_in_db = get_user_from_token(
    security_scopes=security_scopes,
    db=db,
    token=token,
  )

  # try:
  #   payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
  #   print("get_current_user > payload : ", payload)
  #   username: str = payload.get("sub")
  #   print("get_current_user > username : ", username)
  #   if username is None:
  #     raise credentials_exception
  #   token_scopes = payload.get("scopes", [])
  #   print("get_current_user > token_scopes : ", token_scopes)
  #   token_data = TokenData(scopes=token_scopes, username=username)
  # except JWTError:
  #   raise credentials_exception
  
  # user_in_db = user.get_user_by_email(db, email=token_data.username)
  # if user is None:
  #   raise credentials_exception
  # for scope in security_scopes.scopes:
  #   if scope not in token_data.scopes:
  #     raise HTTPException(
  #       status_code=status.HTTP_401_UNAUTHORIZED,
  #       detail="Not enough permissions",
  #       headers={"WWW-Authenticate": authenticate_value},
  #     )

  print("\n")
  return user_in_db


async def get_current_user_optional(
  security_scopes: SecurityScopes,
  db: Session = Depends(get_db),
  token: str = Depends(oauth2_scheme_optional)
  ):
  print("\nget_current_user_optional > security_scopes.scopes : ", security_scopes.scopes)

  if token:
    user_in_db = get_user_from_token(
      security_scopes=security_scopes,
      db=db,
      token=token,
    )
    # try:
    #   payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #   print("get_current_user_optional > payload : ", payload)
    #   username: str = payload.get("sub")
    #   print("get_current_user_optional > username : ", username)
    #   if username is None:
    #     raise credentials_exception
    #   token_scopes = payload.get("scopes", [])
    #   print("get_current_user_optional > token_scopes : ", token_scopes)
    #   token_data = TokenData(scopes=token_scopes, username=username)
    # except JWTError:
    #   raise credentials_exception
    
    # user_in_db = user.get_user_by_email(db, email=token_data.username)
    # if user is None:
    #   raise credentials_exception
    # for scope in security_scopes.scopes:
    #   if scope not in token_data.scopes:
    #     raise HTTPException(
    #       status_code=status.HTTP_401_UNAUTHORIZED,
    #       detail="Not enough permissions",
    #       headers={"WWW-Authenticate": authenticate_value},
    #    )
  
  else:
    user_in_db = None

  print("\n")
  return user_in_db


async def get_current_active_user(
  current_user: User = Security(
    get_current_user,
    scopes=["me"]
    )
  ):
  print("get_current_active_user > current_user : ", current_user)
  if not current_user.is_active:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      msg="Inactive user",
      detail="Inactive user"
    )
  return current_user


async def get_current_active_user_refresh(
  current_user: User = Security(
    get_current_user,
    scopes=["refresh"]
    )
  ):
  print("get_current_active_user_refresh > current_user : ", current_user)
  if not current_user.is_active:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      msg="Inactive user",
      detail="Inactive user"
    )
  return current_user


### USER CLASS

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):


  def get_user_by_email(
    self, db: Session, 
    email: str
    ):
    # print("get_user_by_email > email : ", email)
    return db.query(User).filter(User.email == email).first()


  def get_user_by_id(
    self, db: Session, 
    id: int
    ):
    # print("get_user_by_id > id : ", id)
    return db.query(User).filter(User.id == id).first()


  def authenticate_user(
    self, db: Session,
    user_email: str,
    password: str
    ):
    print("authenticate_user > user_email : ", user_email)
    user_in_db = self.get_user_by_email(db, user_email)
    print("authenticate_user > user_in_db : ", user_in_db.__dict__)
    if not user_in_db:
      return False
    if not verify_password(password, user_in_db.hashed_password):
      return False
    return user_in_db


  def create_user_in_db(
    self, db: Session,
    user_in: UserCreate,
    superuser: bool = False
    ):
    print("create_user_in_db > user_in : ", user_in)
    db_user = User(
      email=user_in.email,
      username=user_in.username,
      name=user_in.name,
      surname=user_in.surname,
      locale=user_in.locale,
      hashed_password=get_password_hash(user_in.password),
      is_active=superuser,
      is_superuser=superuser,
      read=user_in.read
    )
    print("create_user_in_db > db_user : ", db_user)
    self.create(db=db, obj_in=db_user)
    # db.add(db_user)
    # db.commit()
    # db.refresh(db_user)
    return db_user


  def remove_user(
    self, db: Session,
    user_id: int, 
    current_user: User, 
    ):
    # query = users.delete().where(users.c.id == user.id)
    # await database.execute(query)
    # return user_id

    ### check if user has the right to delete another user or itself
    print("delete_user_in_db > current_user :")
    pp.pprint(current_user.__dict__)

    self.remove(db=db, id=user_id, current_user=current_user)
    # if current_user.is_superuser or current_user.id == user_id:
    #   obj = db.query(User).get(user_id)
    #   print("delete_user_in_db > obj :")
    #   if not obj:
    #     raise HTTPException(
    #       status_code=status.HTTP_404_NOT_FOUND,
    #       detail="User not found"
    #     )
    #   pp.pprint(obj.__dict__)
    #   db.delete(obj)
    #   db.commit()
    #   return obj
    # else:
    #   raise HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="You are not authorized to delete an user other than yourself"
    #   )


user = CRUDUser(User)



###  USER FUNCTIONS


# def update_user_field_in_db(
#   db: Session,
#   user_id: int,
#   field: str,
#   value: any
#   ):
#   print("update_user_in_db > field : ", field)
#   print("update_user_in_db > value : ", value)
#   if field not in FIELDS_UPDATE:
#     raise HTTPException(
#       status_code=status.HTTP_401_UNAUTHORIZED,
#       detail="Field not open to update"
#     )
#   db_user = get_user_by_id(db=db, user_id=user_id)
#   print("update_user_in_db > db_user : ", db_user)
#   setattr(db_user, field, value)
#   db.add(db_user)
#   db.commit()
#   db.refresh(db_user)
#   return db_user


# def delete_user_in_db(
#   db: Session,
#   user_id: int, 
#   current_user: User, 
#   ):
#   # query = users.delete().where(users.c.id == user.id)
#   # await database.execute(query)
#   # return user_id

#   ### check if user has the right to delete another user or itself
#   print("delete_user_in_db > current_user :")
#   pp.pprint(current_user.__dict__)

#   if current_user.is_superuser or current_user.id == user_id:
#     obj = db.query(User).get(user_id)
#     print("delete_user_in_db > obj :")
#     if not obj:
#       raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="User not found"
#       )
#     pp.pprint(obj.__dict__)
#     db.delete(obj)
#     db.commit()
#     return obj
#   else:
#     raise HTTPException(
#       status_code=status.HTTP_401_UNAUTHORIZED,
#       detail="You are not authorized to  delete user other than yourself"
#     )


# def create_user_in_db(db: Session, user: UserCreate, superuser: bool = False):
#   print("create_user_in_db > user : ", user)
#   db_user = User(
#     email=user.email,
#     username=user.username,
#     name=user.name,
#     surname=user.surname,
#     locale=user.locale,
#     hashed_password=get_password_hash(user.password),
#     is_active=superuser,
#     is_superuser=superuser,
#   )
#   print("create_user_in_db > db_user : ", db_user)
#   db.add(db_user)
#   db.commit()
#   db.refresh(db_user)
#   return db_user



### USERS FUNCTIONS

# def get_users(db: Session, skip: int = 0, limit: int = 100):
#   return db.query(User).offset(skip).limit(limit).all()

