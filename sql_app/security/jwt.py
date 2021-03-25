import os

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes


### JWT CONFIG

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRES"))

pwd_context = CryptContext(
  schemes=["bcrypt"],
  deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(
  tokenUrl="users/token",
  scopes={
    "me": "Read information about the current user.",
    # "items": "Read items."
  },
)