import logging
from pathlib import Path
from typing import Any, Dict, Optional

import emails
from emails.template import JinjaTemplate

from ..core.config import settings

import pprint
pp = pprint.PrettyPrinter(indent=1)


cwd = Path.cwd()
server_host = settings.SERVER_HOST
api_version = settings.API_V1_STR

smtp_options = {
  "host": settings.SMTP_HOST,
  "port": settings.SMTP_PORT
}
if settings.SMTP_TLS:
  smtp_options["tls"] = True
if settings.SMTP_USER:
  smtp_options["user"] = settings.SMTP_USER
if settings.SMTP_PASSWORD:
  smtp_options["password"] = settings.SMTP_PASSWORD



def send_email(
  email_to: str,
  subject_template: str = "",
  html_template: str = "",
  environment: Dict[str, Any] = {},
  ):

  # print(">>>  send_email > settings : ...")
  # pp.pprint(settings.dict())

  assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
  
  with open(Path(f'{cwd}{settings.EMAIL_TEMPLATES_DIR}') / html_template ) as f:
    template_str = f.read()

  subject = JinjaTemplate(subject_template)
  template = JinjaTemplate(template_str)
  print(">>>  send_email > template : ...",  template)

  message = emails.Message(
    subject=subject,
    html=template,
    mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
  )
  
  response = message.send(
    to=email_to,
    render=environment,
    smtp=smtp_options
  )
  logging.info(f"send email result: {response}")


def send_test_email(
  email_to: str
  ):
  project_name = settings.PROJECT_NAME
  subject = f"{project_name} - Test email"
  html_template = "test_email.html"
  send_email(
    email_to=email_to,
    subject_template=subject,
    html_template=html_template,
    environment={
      "project_name": settings.PROJECT_NAME,
      "email": email_to
    },
  )


def send_reset_password_email(
  email_to: str,
  email: str,
  token: str
  ):
  project_name = settings.APP_TITLE
  subject = f"{project_name} - Password recovery for user {email}"
  print(">>> send_reset_password_email > cwd : ", cwd )
  html_template = "reset_password.html"
  link = f"{server_host}/{api_version}/users/reset-password?token={token}"
  send_email(
    email_to=email_to,
    subject_template=subject,
    html_template=html_template,
    environment={
      "project_name": project_name,
      "username": email,
      "email": email_to,
      "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
      "link": link,
    },
  )


def send_new_account_email(
  email_to: str,
  name: str,
  surname: str,
  username: str,
  password: str,
  token: str
  ):
  project_name = settings.APP_TITLE
  subject = f"{project_name} - New account for user {username}"
  html_template = "new_account.html"
  # link = f"{settings.SERVER_HOST}/verify-email?token={token}"
  link = f"{settings.SERVER_FRONT}/verify-email?token={token}"
  send_email(
    email_to=email_to,
    subject_template=subject,
    html_template=html_template,
    environment={
      "project_name": project_name,
      "name": name,
      "surname": surname,
      "username": username,
      "password": password,
      "email": email_to,
      "link": link,
    },
  )

