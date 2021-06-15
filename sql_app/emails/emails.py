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
  # print(">>>  send_email > template : ...",  template)
  # print("send_email > email_to : ", email_to)
  # print("send_email > subject : ", subject)
  # print("send_email > settings.EMAILS_FROM_EMAIL : ", settings.EMAILS_FROM_EMAIL)
  # print("send_email > environment : ", environment)
  # print("send_email > subject_template : ", subject_template)
  # print("send_email > html_template : ", html_template)

  message = emails.Message(
    subject=subject,
    html=template,
    # mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    mail_from=(settings.EMAILS_FROM_EMAIL),
  )
  print("send_email > message : ", message)

  response = message.send(
    to=email_to,
    render=environment,
    smtp=smtp_options
  )
  print("send_email > response : ", response)
  logging.info(f"send email > result: {response}")


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
  user: Any,
  token: str
  ):
  project_name = settings.APP_TITLE
  subject = f"{project_name} - Password recovery for user {email_to}"
  html_template = "reset_password.html"
  # link = f"{server_host}/{api_version}/users/reset-password?token={token}"
  link = f"{settings.SERVER_FRONT}/reset-password?token={token}&user={email_to}"
  send_email(
    email_to=email_to,
    subject_template=subject,
    html_template=html_template,
    environment={
      "project_name": project_name,
      "username": user.username,
      "name": user.name,
      "surname": user.surname,
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
      "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
      "link": link,
    },
  )


def send_invitation_email(
  email_from: str,
  name: str,
  surname: str,
  username: str,
  token: str,
  invitation: Any,
  ):
  project_name = settings.APP_TITLE
  subject = f"{project_name} - New invitation from {username}"
  html_template = "new_invitation.html"
  item_type = invitation["invitation_to_item_type"]
  item_id = invitation["invitation_to_item_id"]
  link = f"{settings.SERVER_FRONT}/{item_type}/{item_id}?token={token}"
  send_email(
    email_to=invitation["invitee"],
    subject_template=subject,
    html_template=html_template,
    environment={
      "project_name": project_name,
      "email_from": email_from,
      "name": name,
      "surname": surname,
      "username": username,
      "invitation": invitation,
      "link": link,
    },
  )

