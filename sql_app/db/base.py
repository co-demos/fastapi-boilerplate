# Import all the models, so that Base has them before being
# imported by Alembic
from .base_class import Base  # noqa
from ..models.models_item import Item  # noqa
from ..models.models_user import User  # noqa
