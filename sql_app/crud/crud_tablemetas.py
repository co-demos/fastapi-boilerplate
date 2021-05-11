from . import (pp, Session)

from typing import List

from ..db.database import get_db

from .base import CRUDBase
from ..models.models_tablemeta import Tablemeta
from ..schemas.schemas_tablemeta import TablemetaCreate, TablemetaUpdate

from ..models.models_tabledata import TableDataBuilder


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
    tablemeta_id: int,
    skip: int = 0, limit: int = 100
    ):
    """
    Get table_data (in engine_data) from a table_meta object (in engin_commons)
    """

    table_meta_in_db = self.get_by_id(db, tablemeta_id)
    # print("\n...CRUDTablemeta > get_table_data > table_meta_in_db :", table_meta_in_db )

    table_data_uuid = table_meta_in_db.table_data_uuid
    table_data_fields = table_meta_in_db.table_fields
    # print("\n...CRUDTablemeta > get_table_data > table_data_uuid :", table_data_uuid )
    # print("\n...CRUDTablemeta > get_table_data > table_data_fields :", table_data_fields )

    ### 1/ recreate model from fields and table_data uuid
    table_data_obj = TableDataBuilder(db, table_data_uuid, table_data_fields)
    # print("\n...CRUDTablemeta > get_table_data > table_data_obj :", table_data_obj )

    table_data_model = table_data_obj.get_table_model
    # print("\n...CRUDTablemeta > get_table_data > table_data_model :", table_data_model )

    ### 2/ query db with model
    table_data = (
      db.query(table_data_model["model_"])
      .offset(skip)
      .limit(limit)
      .all()
    )
    return table_data 


tablemeta = CRUDTablemeta(Tablemeta)


