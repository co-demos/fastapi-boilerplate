print(">>>>>> import crud.base.py ...")
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from sqlalchemy import and_, or_, not_
from sqlalchemy.orm import Session

from ..db.base_class import BaseCommons
from ..models.models_user import User
from ..schemas.schemas_choices import OperatorType

ModelType = TypeVar("ModelType", bound=BaseCommons)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
  def __init__(self, model: Type[ModelType]):
    """
    CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    **Parameters**

    * `model`: A SQLAlchemy model class
    * `schema`: A Pydantic model (schema) class
    """
    self.model = model

  def get_by_id(
    self, db: Session, 
    id: Any
    ) -> Optional[ModelType]:
    return db.query(self.model).filter(self.model.id == id).first()

  def get_by_title(
    self, db: Session,
    title: str
    ) -> ModelType:
    return db.query(self.model).filter(self.model.title == title).first()

  def get_multi(
    self, db: Session, *, 
    skip: int = 0,
    limit: int = 100,
    ) -> List[ModelType]:
    return (
      db.query(self.model)
      .offset(skip)
      .limit(limit)
      .all()
    )

  def get_multi_by_owner(
    self, db: Session, *,
    owner_id: int,
    skip: int = 0,
    limit: int = 100,
    ) -> List[ModelType]:
    return (
      db.query(self.model)
      .filter(self.model.owner_id == owner_id)
      .offset(skip)
      .limit(limit)
      .all()
    )

  def search_multi_by_fields(
    self, db: Session, *, 
    q: str,
    fields: List[str],
    auth_level: str,
    skip: int = 0,
    limit: int = 100,
    operator: OperatorType = OperatorType.or_,
    ) -> List[ModelType]:
    
    print("\nsearch_multi_by_fields > q : ", q)
    print("search_multi_by_fields > auth_level : ", auth_level)
    print("search_multi_by_fields > fields : ", fields)
    print("search_multi_by_fields > self.model : ", self.model)
    # print("search_multi_by_fields > self.model.__dict__ : ", self.model.__dict__)

    db_query = db.query(self.model)
    results = db_query
    # print("search_mu/lti_by_fields > results - 1 : ", results)

    search_args = []
    for field in fields : 
      column = getattr(self.model, field, None)
      filter_col = column.ilike(f"%{q}%") ### substring match
      # filter_col = column.contains(q) ### exact match
      search_args.append(filter_col)
    print("search_multi_by_fields > search_args : ", search_args)
    
    if operator == "or" :
      filter_arg = or_(*search_args)
    if operator == "not" :
      filter_arg = not_(*search_args)
    if operator == "and" :
      filter_arg = and_(*search_args)

    results_all = (
      db_query
      .filter(
        filter_arg
      )
    )
    results_count = results_all.count()
    print("search_multi_by_fields > results_count : ", results_count)

    results = (
      results_all
      .offset(skip)
      .limit(limit)
      .all()
    )

    print("search_multi_by_fields > results - end : ", results)
    return results, results_count

  def create(
    self, db: Session, *, 
    obj_in: CreateSchemaType
    ) -> ModelType:
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = self.model(**obj_in_data)  # type: ignore
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

  def create_with_owner(
    self, db: Session, *, 
    obj_in: CreateSchemaType,
    owner_id: int
    ) -> ModelType:
    print("\ncreate_with_owner > obj_in : ", obj_in)
    obj_in_data = jsonable_encoder(obj_in)
    print("\ncreate_with_owner > obj_in_data : ", obj_in_data)
    # print("\ncreate_with_owner > self.model : ", self.model)
    db_obj = self.model(**obj_in_data, owner_id=owner_id)
    # print("\ncreate_with_owner > db_obj : ", db_obj)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

  def update(
    self, db: Session, *,
    db_obj: ModelType,
    obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
    obj_data = jsonable_encoder(db_obj)
    print("update > isinstance(obj_in, dict) : ", isinstance(obj_in, dict))
    if isinstance(obj_in, dict):
      update_data = obj_in
    else:
      update_data = obj_in.dict(exclude_unset=True)
    for field in obj_data:
      if field in update_data:
        setattr(db_obj, field, update_data[field])
    print("update > db_obj : ", db_obj)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

  def remove(
    self, db: Session, *,
    id: int,
    current_user: User,
    ) -> ModelType:
    print("remove > id : ", id)
    print("remove > current_user.id : ", current_user.id)
    obj = db.query(self.model).get(id)
    if not obj:
      raise HTTPException(status_code=404, detail="object not found")
    # print("remove > current_user.__dict__ : ", current_user.__dict__)
    # if not current_user.is_superuser and (obj.owner_id == current_user.id):
    #   raise HTTPException(status_code=400, detail="Not enough permissions")
    print("remove > END > obj : ", obj)
    db.delete(obj)
    db.commit()
    return obj
