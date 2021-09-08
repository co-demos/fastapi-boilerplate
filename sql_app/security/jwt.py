from ..core.config import settings

from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes

# print('>>> OAuth2PasswordRequestForm : ', OAuth2PasswordRequestForm.__dict__)

### JWT CONFIG

SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.JWT_EXPIRES)
REFRESH_TOKEN_EXPIRE_MINUTES = int(settings.JWT_REFRESH_EXPIRES_DAYS * 24 * 60 )

pwd_context = CryptContext(
  schemes=["bcrypt"],
  deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(
  tokenUrl="users/token",
  scopes={
    "me": "Read information about the current user.",

    "shared": "Shared data.",

    "read": "Read data.",
    "comment": "Comment data.",
    "patch": "patch data.",
    "manage": "Manage data.",

    "refresh": "Refresh token scope.",
  },
)


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


def generate_password_reset_token(email: str) :
  delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
  now = datetime.utcnow()
  expires = now + delta
  exp = expires.timestamp()
  encoded_jwt = jwt.encode(
    {
      "exp": exp, 
      "nbf": now,
      "sub": email
    }, 
    SECRET_KEY,
    algorithm=ALGORITHM,
  )
  return encoded_jwt


def generate_invit_token(email: str) :
  delta = timedelta(days=settings.INVITATION_TOKEN_EXPIRE_DAYS)
  now = datetime.utcnow()
  expires = now + delta
  exp = expires.timestamp()
  encoded_jwt = jwt.encode(
    {
      "exp": exp, 
      "nbf": now,
      "sub": email
    }, 
    SECRET_KEY,
    algorithm=ALGORITHM,
  )
  return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
  print("verify_password_reset_token > token : ", token)
  try:
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print("verify_password_reset_token > decoded_token : ", decoded_token)
    return decoded_token["sub"]
  except jwt.JWTError:
    return None


def verify_invit_token(token: str) -> Optional[str]:
  print("verify_invit_token > token : ", token)
  try:
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print("verify_invit_token > decoded_token : ", decoded_token)
    return decoded_token["sub"]
  except jwt.JWTError:
    return None
