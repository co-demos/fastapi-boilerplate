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
    """
    Get all table_meta related to a dataset object
    """
    print("\n...CRUDTablemeta > get_multi_by_dataset > dataset_id :", dataset_id )
    print("...CRUDTablemeta > get_multi_by_dataset > self.model :", self.model )

    return (
      db.query(self.model)
      .filter(self.model.dataset_id == dataset_id)
      .offset(skip)
      .limit(limit)
      .all()
    )
  
  def get_table_data(
    self, db: Session,
    skip: int = 0, limit: int = 100
    ):
    """
    Get table_data (in engine_data) from a table_meta object (in engin_commons)
    """
    print("\n...CRUDTablemeta > get_table_data > self.model.id :", self.model.id )

tablemeta = CRUDTablemeta(Tablemeta)


