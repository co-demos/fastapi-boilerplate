import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator

import pprint
pp = pprint.PrettyPrinter(indent=4)

class Settings(BaseSettings):
  API_V1_STR: str = "/api/v1"
  SECRET_KEY: str = secrets.token_urlsafe(32)
  SERVER_HOST: AnyHttpUrl

  JWT_SECRET_KEY: str
  JWT_ALGORITHM: str
  JWT_EXPIRES: int
  # ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
  # 60 minutes * 24 hours * 8 days = 8 days

  # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
  # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
  # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
  # BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
  BACKEND_CORS_ORIGINS: List[Any] = []
  # @validator("BACKEND_CORS_ORIGINS", pre=True)
  # def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
  #   if isinstance(v, str) and not v.startswith("["):
  #     return [i.strip() for i in v.split(",")]
  #   elif isinstance(v, (list, str)):
  #     return v
  #   raise ValueError(v)

  APP_TITLE: str
  APP_DESCRIPTION: str
  APP_VERSION: str

  # SENTRY_DSN: Optional[HttpUrl] = None
  # @validator("SENTRY_DSN", pre=True)
  # def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
  #   if len(v) == 0:
  #     return None
  #   return v

  SQL_TYPE: str
  SQLITE_DB_NAME: str
  SQLITE_DB_URL: str
  SQLITE_DB_URL_ALEMBIC: str

  SQL_SERVER: str
  SQL_USER: str
  SQL_PWD: str
  SQL_DB: str
  SQL_DB_URL: str
  SQL_DB_URL_BIS: Optional[PostgresDsn] = None

  @validator("SQL_DB_URL_BIS", pre=True)
  def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
    if isinstance(v, str):
      return v
    return PostgresDsn.build(
      scheme="postgresql",
      user=values.get("SQL_USER"),
      password=values.get("SQL_PWD"),
      host=values.get("SQL_SERVER"),
      path=f"/{values.get('SQL_DB') or ''}",
    )

  SMTP_TLS: bool = True
  SMTP_PORT: Optional[int] = None
  SMTP_HOST: Optional[str] = None
  SMTP_USER: Optional[str] = None
  SMTP_PASSWORD: Optional[str] = None
  EMAILS_FROM_EMAIL: Optional[EmailStr] = None
  EMAILS_FROM_NAME: Optional[str] = None

  @validator("EMAILS_FROM_NAME")
  def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
    if not v:
      return values["APP_TITLE"]
    return v

  EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
  EMAIL_TEMPLATES_DIR: str = "/sql_app/emails/email-templates/build"
  EMAILS_ENABLED: bool = False

  @validator("EMAILS_ENABLED", pre=True)
  def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
    return bool(
      values.get("EMAIL_ENABLED")
      and values.get("SMTP_HOST")
      and values.get("SMTP_PORT")
      and values.get("EMAILS_FROM_EMAIL")
    )

  EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
  FIRST_SUPERUSER: EmailStr
  FIRST_SUPERUSER_PASSWORD: str
  USERS_OPEN_REGISTRATION: bool = False

  class Config:
    case_sensitive = True
    env_file = '../.env'
    env_file_encoding = 'utf-8'

settings = Settings()
print("config.py > settings : ...")
pp.pprint(settings.dict())
