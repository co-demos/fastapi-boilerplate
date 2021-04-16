### for working example of JSON column type check : https://github.com/tiangolo/fastapi/issues/211
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy_utils import EmailType, URLType
from sqlalchemy.orm import relationship

import datetime
