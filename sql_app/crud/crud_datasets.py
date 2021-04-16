from . import (pp, Session)

from ..db.database import get_db

from .base import CRUDBase
from ..models.models_dataset import Dataset
from ..schemas.schemas_dataset import DatasetCreate, DatasetUpdate


class CRUDDataset(CRUDBase[Dataset, DatasetCreate, DatasetUpdate]):
  pass

workspace = CRUDDataset(Dataset)


