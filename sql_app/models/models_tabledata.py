from fastapi.encoders import jsonable_encoder
from sqlalchemy import (
  Table, MetaData, Column, ForeignKey, 
  Boolean, Integer, String, Float, DateTime, JSON
)
from sqlalchemy_utils import EmailType, URLType, get_class_by_table

from ..db.database import engine_commons, engine_data
from ..db.base_class import BaseData

from sqlalchemy.orm import mapper
from sqlalchemy.ext.declarative import ( 
  declarative_base, 
  as_declarative, 
  declared_attr 
)

from pydantic import BaseModel, create_model, EmailStr, Json, AnyUrl
from pydantic.color import Color
from typing import List, Optional, Any, Union
import datetime

from ..crud.base import CRUDBase


import pprint
pp = pprint.PrettyPrinter(indent=1)

metadata = MetaData(bind=engine_data, reflect=True)

table_model_prefix = "DP_"
table_field_prefix = "f_"
table_base_prefix = "BASE_"

field_types = {
  "str":     { "model": String,     "schema": str },
  "longStr": { "model": String,     "schema": str },
  "int":     { "model": Integer,    "schema": int },
  "float":   { "model": Float,      "schema": float },
  "bool":    { "model": Boolean,    "schema": bool },
  "date":    { "model": String,     "schema": Union[str, datetime.datetime] },
  "tag":     { "model": String,     "schema": Union[str, List[str]] },
  "rating":  { "model": String,     "schema": str },
  "url":     { "model": URLType,    "schema": AnyUrl },
  "email":   { "model": EmailType,  "schema": EmailStr },
  "latlon":  { "model": String,     "schema": Union[str, tuple] },
  "json":    { "model": JSON,       "schema": Any },
  "html":    { "model": String,     "schema": str },
  "md":      { "model": String,     "schema": str },
  "curr":    { "model": Float,      "schema": float },
  "ref":     { "model": String,     "schema": str },
  "refs":    { "model": String,     "schema": str },
  "color":   { "model": String,     "schema": Color },
  "any":     { "model": String,     "schema": Any },
}


################################
### MODEL - sqlalchemy
################################

class TableDataModel:
  """
    Creates a SqlAlchemy model dynamically given a list of fields.
      
    Attributes:
    ----------
      [ <sqlalchemy type> ] : list of sqlachemy types
  """
  
  # id = Column(Integer, primary_key=True, autoincrement=True),

  def __init__(self, table_fields):
    """
      The constructor for TableDataModel class.

      Parameters
      ----------
        table_fields (list of dicts): ...
    """
    # print("=== TableData > table_fields :", table_fields)
    for col in table_fields:
      col_id = f"{table_field_prefix}{col['id']}"
      col_type = col["field_type"]
      # print("\n=== TableDataModel > col_id :", col_id)
      # print("=== TableDataModel > col_type :", col_type)
      self.__dict__[col_id] = Column(col_id, field_types[col_type]["model"])

  # @property
  # def allColumns(self) : 
  #   """
  #   Returns a list of Column objects from self.
  #   """
  #   # print("\n=== TableDataModel > allColumns ... ")
  #   all_columns = self.__dict__.keys()
  #   return [ self.__dict__[item] for item in all_columns if not item.startswith("_")]


################################
### SCHEMA 
################################

# constructor
def TableDataBaseConstructor(table_fields):
  """
    The constructor for TableDataBase class.
    ### cf : https://pydantic-docs.helpmanual.io/usage/models/#required-optional-fields

    Parameters
    ----------    
    table_fields : [ dict ]
      The fields (or headers) populating the columns.
      List of field objects, each containing at least those keys : 'id', 'field_type', 'value'
  """
  pydantic_fields = {}
  for col in table_fields:
    # print("\n=== TableDataBaseConstructor > col :", col)
    col_id = f"{table_field_prefix}{col['id']}"
    col_type = col["field_type"]
    # pydantic_fields[col_id] = (Optional[field_types[col_type]["schema"]], ... )
    pydantic_fields[col_id] = (Optional[field_types[col_type]["schema"]], None )
  return pydantic_fields

def CreateTableDataBase(table_uuid, table_fields):
  """
    Creates a Pydantic schema class dynamically.
      
    Parameters
    ----------
    table_uuid : str
      The table_uuid given to the dynamically created table
    table_fields : [ dict ]
      The fields (or headers) populating the columns.
      List of field objects, each containing at least those keys : 'id', 'field_type', 'value'
    
    Return:
    ----------
      tableSchemaClass : Dynamically created pydantic model

    ### cf : https://www.geeksforgeeks.org/create-classes-dynamically-in-python/#:~:text=Python%20Code%20can%20be%20dynamically,the%20type%20of%20the%20object.&text=The%20above%20syntax%20returns%20the%20type%20of%20object.
  """
  print("\n=== CreateTableDataBase > table_uuid :", table_uuid)
  # print("=== CreateTableDataBase > table_fields :", table_fields)

  fields = TableDataBaseConstructor(table_fields)
  tableSchemaClass = create_model(
    f"{table_base_prefix}{table_uuid}",
    **fields
  )
  
  print("\n=== CreateTableDataBase > tableSchemaClass.__name__ :", tableSchemaClass.__name__)
  return tableSchemaClass

def CreateFieldsCodes(table_fields): 
  fields_with_code = [ { **f, "field_code": f"{table_field_prefix}{f['id']}" } for f in table_fields ]
  return fields_with_code


################################
### DB TABLE - BUILDER + CRUD
################################

class TableDataBuilder(object):

  def __init__(self, db, table_uuid, table_fields):
    """
      Build a full table object dynamically, usable as models, schema, ...
      Methods can either create a new table in the DB given a list of columns, 
      can operate CRUD operations on said table,
      can populate the table with data,
      can make CRUD operations on data,
      ...

      Parameters
      ----------
      table_uuid : str
        The UUID for the created table or for the table to create
      table_fields : [ dict ]
        The fields (or headers) populating the columns.
        List of field objects, each containing at least those keys : 'id', 'field_type', 'value'
    """
    print("\n================================================================= ")
    print("\n=== TableDataBuilder > init > table_uuid :", table_uuid)
    # print("\n=== TableDataBuilder > init > stable_fields :", table_fields)

    self.db = db
    self.table_uuid = table_uuid
    self.table_name = f"{table_model_prefix}{self.table_uuid}"
    
    # build specific data
    self.table_fields = table_fields
    self.table_structure = TableDataModel(table_fields)
    self.table_schema = CreateTableDataBase(table_uuid, table_fields)

  ### ---------------------------------------------- ###
  ### table objects (SQL model + Pydantic) creation
  ### ---------------------------------------------- ###

  # @property
  # def table_columns(self):
  #   return self.table_structure.allColumns

  def build_model(self, only_get=False, table=None): 
    args_dict = {
      "__tablename__": self.table_name,
      # "__table_args__": {'extend_existing': True},
      "id": Column(Integer, primary_key=True, autoincrement=True),
      **self.table_structure.__dict__
    }
    if only_get:
      args_dict["__tablename__"] = table
      args_dict["__table_args__"] = {'extend_existing': True}
    Model = type(self.table_name, (BaseData,), args_dict)
    return Model
  
  # def get_model(self, table): 
  #   Model = type(self.table_name, (BaseData,), {
  #     "__tablename__": table,
  #     "__table_args__": {'extend_existing': True},
  #     "id": Column(Integer, primary_key=True, autoincrement=True),
  #     **self.table_structure.__dict__
  #     }
  #   )
  #   return Model

  @property
  def get_table_model(self):

    # model = None

    print("\n=== === ==== ==== \n=== TableDataBuilder > get_table_model > self.table_name :", self.table_name)
    # pp.pprint(dir(metadata))

    # print("\n=== TableDataBuilder > get_table_model > self.db ... ")
    # pp.pprint( vars(self.db) )

    try : 
      print("\n=== TableDataBuilder > get_table_model > A1 > metadata.tables ... ")
      meta_table = metadata.tables[self.table_name]
      # print("\n=== TableDataBuilder > get_table_model > A2 > meta_table.__dict__ ... ")
      # pp.pprint( meta_table.__dict__ )
      # print("\n=== TableDataBuilder > get_table_model > A2 > meta_table ... ")
      # pp.pprint( dir(meta_table.c) )

      print("\n=== TableDataBuilder > get_table_model > A3 > get_model ... ")
      model_ = self.build_model(only_get=True, table=meta_table)
      # pp.pprint( model_.__dict__ )

    # print("\n=== TableDataBuilder > get_table_model > A3 > meta_table.columns ... ")
    # print( meta_table.columns )

    # print("\n=== TableDataBuilder > get_table_model > D1 > self.table_schema ... ")
    # print( self.table_schema.__dict__ )
    # model = self.table_schema 

    # print("\n=== TableDataBuilder > get_table_model > B1 > self.db ... ")
    # print( dir(self.db) )
    # pp.pprint( self.db.__dict__ )

    # print("\n=== TableDataBuilder > get_table_model > B1 > BaseData ... ")
    # pp.pprint( BaseData.__dict__ )
    # print("\n=== TableDataBuilder > get_table_model > B2 > BaseData._decl_class_registry.values() ... ")
    # pp.pprint( BaseData._decl_class_registry.values() )
    # for c in BaseData._decl_class_registry.values():
    #   print("=== TableDataBuilder > try > get_table_model > c ... ")
    #   pp.pprint( c )
    #   if hasattr(c, '__tablename__') :
    #     pp.pprint(c.__tablename__)
    #     if c.__tablename__ == self.table_name:
    #       pp.pprint( c.__dict__ )
    #       # pp.pprint( dir(c) )
    #       model = c
    
    except : 
      ### exception if server has reloaded
      print("\n=== TableDataBuilder > get_table_model > self.build_model() > model ... ")
      model_ = self.build_model(only_get=True, table=self.table_name)

    # print("\n=== TableDataBuilder > get_table_model > model ... ")
    # pp.pprint(model.__dict__)
    return {
      # "model": model,
      "model_": model_,
      # "columns": meta_table.c,
      # "table": meta_table,
    }


  def create_table(self):
    """
    Build the Table object and create it in the DB
    cf : https://docs.sqlalchemy.org/en/14/core/metadata.html
    cf : https://stackoverflow.com/questions/973481/dynamic-table-creation-and-orm-mapping-in-sqlalchemy
    """
    self.table_model = self.build_model()
    print("\n=== TableDataBuilder > cols_mapper > self.table_model :", self.table_model)
    BaseData.metadata.create_all(bind=engine_data)


  ### ---------------------- ###
  ### table data population
  ### ---------------------- ###

  @property
  def cols_mapper(self):
    """
    Retrieves a dict to map original field.value in data to field.id in the postgresql table
    Returns:
    -------
      cols : a dictionnary as follow { <field_value> : <field_id> }
    """
    # print("\n=== TableDataBuilder > cols_mapper > self.table_fields :", self.table_fields)
    # cols = { h["value"] : f"{table_field_prefix}{h['id']}" for h in self.table_fields }
    cols = { h["value"] : f"{h['field_code']}" for h in self.table_fields }
    return cols

  def set_table_data(self, table_data):
    """ 
    Remap a table_data (list of dicts) with self.cols_mapper .
    
    Parameters :
    ----------
      table_data ( [dict] ): list of dictionnaries... 
    """
    print("\n=== TableDataBuilder > bulk_import > table_data :", table_data)
    cols_mapper = self.cols_mapper
    print("\n=== TableDataBuilder > bulk_import > cols_mapper :", cols_mapper)

    table_data_ = [ { cols_mapper[k] : data.get(k) for k in cols_mapper.keys() } for data in table_data ]
    # table_data_ = []
    # for data in table_data :
    #   print("\n=== TableDataBuilder > bulk_import > data :", data)
    #   data_ = {}
    #   for k in cols_mapper.keys() :
    #     print("=== TableDataBuilder > bulk_import > k :", k)
    #     data_[ cols_mapper[k] ] = data.get(k)
    #     table_data_.append(data_)
    self.table_data = table_data_

  def bulk_import(self, table_data):
    """ 
    Save table_data to DB.

    Parameters :
    ----------
      table_data ( [dict] ): list of dictionnaries... 
    """
    self.set_table_data(table_data)
    # print("\n=== TableDataBuilder > bulk_import > self.table_data :", self.table_data)
    # print("\n=== TableDataBuilder > bulk_import > self.table_schema :", self.table_schema )
    # print("\n=== TableDataBuilder > bulk_import > self.table_schema.__dict__ ..." )
    # pp.pprint(self.table_schema.__dict__)

    ### parse data with pydantic schema
    objects_in = [ self.table_schema(**data) for data in self.table_data ]
    # print("\n=== TableDataBuilder > bulk_import > objects_in ...")
    pp.pprint(objects_in)

    ### convert data to sqlalchemy model
    objects_in_data = jsonable_encoder(objects_in)
    # print("\n=== TableDataBuilder > bulk_import > objects_in_data ...")
    # pp.pprint(objects_in_data)
    # print(objects_in_data)

    # print("\n=== TableDataBuilder > bulk_import > self.table_model ...")
    # pp.pprint(self.table_model)

    db_objects = [ self.table_model(**obj) for obj in objects_in_data ]

    ### save in new table
    self.db.bulk_save_objects(db_objects)
    # self.db.add_all(db_objects)
    self.db.commit()
    return db_objects
