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

pwd_context = CryptContext(
  schemes=["bcrypt"],
  deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(
  tokenUrl="users/token",
  scopes={
    "me": "Read information about the current user.",
    "items": "Read items.",
    "posts": "Read posts.",
    "comments": "Read comments."
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
    settings.SECRET_KEY,
    algorithm="HS256",
  )
  return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
  try:
    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    return decoded_token["email"]
  except jwt.JWTError:
    return None
