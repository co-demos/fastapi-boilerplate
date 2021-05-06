from . import (pp, Session)

from typing import List

from ..db.database import get_db

from .base import CRUDBase
from ..models.models_tablemeta import Tablemeta
from ..schemas.schemas_tablemeta import TablemetaCreate, TablemetaUpdate


class CRUDTablemeta(CRUDBase[Tablemeta, TablemetaCreate, TablemetaUpdate]):
  
  def get_multi_by_dataset(
    self, db: Session,
    dataset_id: int,
    skip: int = 0, limit: int = 100
    ):

    print("\n...CRUDTablemeta > get_multi_by_dataset > dataset_id :", dataset_id )
    print("...CRUDTablemeta > get_multi_by_dataset > self.model :", self.model )

    return (
      db.query(self.model)
      .filter(self.model.dataset_id == dataset_id)
      .offset(skip)
      .limit(limit)
      .all()
    )

tablemeta = CRUDTablemeta(Tablemeta)


