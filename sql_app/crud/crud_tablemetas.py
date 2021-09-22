from . import (pp, Session)

from typing import List, Dict, Any, Union, Optional
from fastapi.encoders import jsonable_encoder

from ..db.database import get_db

from .base import CRUDBase
from ..models.models_user import User
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
  
  def get_tabledata_model(
    self, db,
    tablemeta_id: int,
    user: User,
    ):
    table_meta_in_db = self.get_by_id(db, tablemeta_id, user=user )
    print("\n...CRUDTablemeta > get_table_data > table_meta_in_db :", table_meta_in_db )
    table_data_uuid = table_meta_in_db.table_data_uuid
    table_data_fields = table_meta_in_db.table_fields
    # print("\n...CRUDTablemeta > get_table_data > table_data_uuid :", table_data_uuid )
    # print("\n...CRUDTablemeta > get_table_data > table_data_fields :", table_data_fields )
    
    ### 1/ recreate model from fields and table_data uuid
    table_data_obj = TableDataBuilder(db, table_data_uuid, table_data_fields)
    # print("\n...CRUDTablemeta > get_table_data > table_data_obj :", table_data_obj )
    table_data_model = table_data_obj.get_table_model
    # print("\n...CRUDTablemeta > get_table_data > table_data_model :", table_data_model )
    return table_data_model

  def get_table_data(
    self, db: Session,
    tablemeta_id: int,
    user: User,
    skip: int = 0, limit: int = 100
    ):
    """
    Get table_data (in engine_data) from a table_meta object (in engin_commons)
    """
    print("\n...CRUDTablemeta > get_table_data > tablemeta_id :", tablemeta_id )

    # table_meta_in_db = self.get_by_id(db, tablemeta_id)
    # table_data_uuid = table_meta_in_db.table_data_uuid
    # table_data_fields = table_meta_in_db.table_fields
    # table_data_obj = TableDataBuilder(db, table_data_uuid, table_data_fields)
    # table_data_model = table_data_obj.get_table_model
    table_data_model = self.get_tabledata_model(db, tablemeta_id, user=user)

    ### 2/ query db with model
    table_data = (
      # db.query(table_data_model["model_"])
      db.query(table_data_model)
      .order_by(table_data_model.id)
      .offset(skip)
      .limit(limit)
      .all()
    )
    return table_data

  def update_table_data_row(
    self, db: Session, *,
    tablemeta_id: int,
    obj_in: Dict[str, Any],
    ):
    """
    Update table_data (in engine_data) from a table_meta object (in engin_commons)
    """
    print("\nupdate_table_data_row > obj_in : ", obj_in)
    obj_data = jsonable_encoder(obj_in)
    print("update_table_data_row > obj_data : ", obj_data)
    
    # table_meta_in_db = self.get_by_id(db, tablemeta_id)
    # table_data_uuid = table_meta_in_db.table_data_uuid
    # table_data_fields = table_meta_in_db.table_fields
    # table_data_obj = TableDataBuilder(db, table_data_uuid, table_data_fields)
    # table_data_model = table_data_obj.get_table_model
    table_data_model = self.get_tabledata_model(db, tablemeta_id)

    if obj_in.update_type == "cell":
      data_in = obj_in.table_data_cell
      row_id = data_in.row_id
      data_in_dict = {}
      data_in_dict[data_in.column] = data_in.value

    if obj_in.update_type == "row":
      data_in = obj_in.table_data_row
      # row_id = obj_in.table_data_row_id
      data_in_dict = data_in

    if obj_in.update_type == "rows":
      data_in = obj_in.table_data_rows
      data_in_dict = data_in.dict()

    print("update_table_data_row > data_in : ", data_in)
    print("update_table_data_row > data_in_dict : ", data_in_dict)

    # update cell
    if obj_in.update_type in ["cell"] :
      db_row = db.query(table_data_model).filter(table_data_model.id == row_id).first()
      print("update_table_data_row > cell > db_row A : ", db_row)
      row_data = jsonable_encoder(db_row)
      print("update_table_data_row > cell > row_data : ", row_data)
      for field in row_data:
        print("update_table_data_row > cell > field : ", field)
        if field in data_in_dict:
          setattr(db_row, field, data_in_dict[field])

    # append a row
    if obj_in.update_type in ["row"] :
      row_data = jsonable_encoder(data_in)
      print("update_table_data_row > row > row_data : ", row_data)
      db_row = table_data_model(**row_data)
      print("update_table_data_row > row > db_row : ", db_row)

    db.add(db_row)
    db.commit()
    db.refresh(db_row)
    return db_row

  def remove_table_data_row(
    self, db: Session, *,
    tablemeta_id: int,
    obj_in: Dict[str, Any],
    ):
    """
    Remove table_data (in engine_data) from a table_meta object (in engin_commons)
    """
    print("\nupdate_table_data_row > obj_in : ", obj_in)
    table_data_model = self.get_tabledata_model(db, tablemeta_id)
    row_id = obj_in.table_data_row_id
    db_row = db.query(table_data_model).filter(table_data_model.id == row_id).first()
    db.delete(db_row)
    db.commit()
    return db_row


tablemeta = CRUDTablemeta(Tablemeta)


