print(">>>>>> import crud.base.py ...")
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from sqlalchemy import and_, or_, not_
from sqlalchemy.orm import Session

from ..db.base_class import BaseCommons
from ..models.models_user import User
from ..models.models_group import Group
from ..schemas.schemas_choices import OperatorType
from ..schemas.schemas_invitation import InvitationBasics, InvitationCreate

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

  def invite(
    self, db: Session, *, 
    db_obj: ModelType,
    obj_in: InvitationBasics,
    invitor: Any
    ) -> ModelType:
    print("\ninvite > db_obj : ", db_obj)
    obj_data = jsonable_encoder(db_obj)
    print("invite > obj_data : ", obj_data)

    obj_owner_id = obj_data["owner_id"]

    obj_authorized_users = obj_data.get("authorized_users", [])
    obj_authorized_groups = obj_data.get("authorized_groups", [])
    authorized_users = obj_authorized_users or []
    authorized_groups = obj_authorized_groups or []

    obj_pending_users = obj_data.get("pending_users", [])
    obj_pending_groups = obj_data.get("pending_groups", [])
    pending_users = obj_pending_users or []
    pending_groups = obj_pending_groups or []

    print("invite > obj_owner_id : ", obj_owner_id)
    print("invite > obj_authorized_users : ", obj_authorized_users)
    print("invite > obj_authorized_groups : ", obj_authorized_groups)

    print("\ninvite > obj_in : ", obj_in)
    basic_invitation = jsonable_encoder(obj_in)
    print("invite > basic_invitation : ", basic_invitation)

    print("\ninvite > invitor : ", invitor)
    invitor_data = jsonable_encoder(invitor)
    print("invite > invitor_data : ", invitor_data)
    invitor_id = invitor.id
    print("invite > invitor_id : ", invitor_id)
    invitor_email = invitor.email
    print("invite > invitor_email : ", invitor_email)

    msg = basic_invitation["message"]

    ### A/ parse invitees ###
    invitations = []
    for invitee in basic_invitation["invitees"] :
      print("\ninvite > invitee : ", invitee)

      ### - create invitations for invitee / user (if not invitor)
      if invitee["invitee_type"] == "user" :
        invitee_email = invitee["invitee_email"]
        if invitor_email != invitee_email and invitee_email not in authorized_users :
          invitation = InvitationCreate(
            **basic_invitation,
            invitee = invitee_email
          )
          print("invite > invitation : ", invitation)
          invitations.append(invitation)
          pending_users.append(invitee_email)

      ### - create invitations for invitee / group
      if invitee["invitee_type"] == "group" :
        # get group's users & emails
        group_id = invitee["invitee_id"]
        group_in_db = db.query(Group).filter(Group.id == group_id).first()
        print("invite > group_in_db : ", group_in_db)

        group_manage_level = group_in_db.manage
        print("invite > group_manage_level : ", group_manage_level)

        group_owner_id = group_in_db.owner_id

        ### invite group owner (if not invitor)
        if group_owner_id not in authorized_groups :
          group_owner_in_db = db.query(User).filter(User.id == group_owner_id).first()
          print("invite > group_owner_in_db : ", group_owner_in_db)
          invitation = InvitationCreate(
            **basic_invitation,
            invitee = group_owner_in_db.email
          )
          invitations.append(invitation)
          pending_groups.append(group_id)

        # group_users = group_in_db.authorized_users
        # print("invite > group_users : ", group_users)


    ### - send invitations to invitee
    print("\ninvite > loop invitations ...")
    for invit in invitations :
      print("invite > invit : ", invit)

    

    ### B/ update invitor data ###
    ### - send email to invitor resuming invitations sent


    ### C/ update object ###
    ### - append every invitee email as pending user
    
    obj_data["pending_users"] = pending_users
    if basic_invitation["invitation_to_item_type"] != "group" :
      obj_data["pending_groups"] = pending_groups
    print("\ninvite > obj_data : ", obj_data)

    # db_obj = self.model(**obj_in_data)
    # print("invite > db_obj : ", db_obj)
    # db.add(db_obj)
    # db.commit()
    # db.refresh(db_obj)

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
