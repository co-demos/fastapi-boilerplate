print(">>>>>> import schemas_token.py >  Token ...")
from typing import List, Optional, Any
import datetime

from pydantic import BaseModel, Field, EmailStr
from uuid import UUID

### TOKEN

class Token(BaseModel):
  token_type: str

class TokenAccess(Token):
  access_token: str

class TokenRefresh(Token):
  refresh_token: str

class TokenAccessRefresh(TokenAccess, TokenRefresh):
  pass

class TokenData(BaseModel):
  username: Optional[str] = None
  scopes: List[str] = []
