print(">>>>>> import crud.base.py ...")
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

import json

from fastapi import HTTPException, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from sqlalchemy import and_, or_, not_, func, tuple_, text, cast
from sqlalchemy.orm import Session
# from sqlalchemy.dialects.postgresql import JSONB
# from sqlalchemy.sql.expression import literal_column

from ..db.base_class import BaseCommons
from ..models.models_user import User
from ..models.models_group import Group
from ..models.models_invitation import Invitation

from ..schemas.schemas_choices import OperatorType
from ..schemas.schemas_invitation import InvitationBasics, InvitationCreate
from ..schemas.schemas_auths import AuthInfos, UserAuthInfos, GroupAuthInfos, UserAuthPending, GroupAuthPending

from ..emails.emails import send_invitation_email

from ..security.jwt import generate_invit_token

ModelType = TypeVar("ModelType", bound=BaseCommons)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

# authorized_users_value = literal_column('authorized_users.value', type_=JSONB)
# user_email_value = literal_column('user_email.value', type_=JSONB)


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

    # return (
    #   db.query(self.model)
    #   .filter(self.model.owner_id == owner_id)
    #   .offset(skip)
    #   .limit(limit)
    #   .all()
    # )

    items_in_db = db.query(self.model).filter(self.model.owner_id == owner_id)

    if skip > 0 :
      items_in_db = items_in_db.offset(skip)
    if limit and limit > 0 :
      items_in_db = items_in_db.limit(limit)

    return items_in_db.all()


  def get_multi_by_authorized_user(
    self, db: Session, *,
    user_id: int,
    user_email: str,
    skip: int = 0,
    limit: int = 100,
    ) -> List[ModelType]:

    print("\nget_multi_by_authorized_user > user_id : ", user_id)
    print("get_multi_by_authorized_user > user_email : ", user_email)
    user_ref = { "user_email": user_email }
    print("get_multi_by_authorized_user > user_ref : ", user_ref)
    
    items_in_db = db.query(self.model).filter(
      self.model.owner_id != user_id, 
      self.model.authorized_users.isnot(None),
    )
    print("get_multi_by_authorized_user > items_in_db.count() : ", items_in_db.count())
    for i in items_in_db.all() :
      print( f"... get_multi_by_authorized_user > {i.id} > i.authorized_users : ", i.authorized_users )

    items_in_db = items_in_db.filter( self.model.authorized_users.contains([user_ref]) )
    print("\nget_multi_by_authorized_user > items_in_db : ", items_in_db)

    if skip > 0 :
      items_in_db = items_in_db.offset(skip)
    if limit and limit > 0 :
      items_in_db = items_in_db.limit(limit)

    return items_in_db.all()


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

    results = results_all
    if skip > 0 :
      results = results.offset(skip)
    if limit and limit > 0 :
      results = results.limit(limit)
    results = results.all()

    # results = (
    #   results_all
    #   .offset(skip)
    #   .limit(limit)
    #   .all()
    # )

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
    # print("\nupdate > isinstance(obj_in, dict) : ", isinstance(obj_in, dict))
    # print("update > obj_in : ", obj_in)
    if isinstance(obj_in, dict):
      update_data = obj_in
    else:
      update_data = obj_in.dict(exclude_unset=True)
    for field in obj_data:
      if field in update_data:
        # print("update > obj_in : ", obj_in)
        setattr(db_obj, field, update_data[field])
    # print("update > db_obj : ", db_obj)
    # print("update > jsonable_encoder(db_obj) : ", jsonable_encoder(db_obj))
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

  def invite(
    self, db: Session, *,
    db_obj: ModelType,
    background_tasks: BackgroundTasks,
    obj_in: InvitationBasics,
    invitor: Any
    ) -> ModelType:
    print("\ninvite > db_obj : ", db_obj)
    obj_data = jsonable_encoder(db_obj)
    print("invite > obj_data : ", obj_data)

    obj_owner_id = obj_data["owner_id"]

    obj_authorized_users = obj_data.get("authorized_users", [])
    obj_authorized_groups = obj_data.get("authorized_groups", [])
    print("invite > obj_authorized_users : ", obj_authorized_users)

    authorized_users = obj_authorized_users or []
    print("invite > authorized_users : ", authorized_users)
    authorized_users_emails = [ i["user_email"] for i in authorized_users ]
    authorized_groups = obj_authorized_groups or []
    authorized_groups_ids = [ i["group_id"] for i in authorized_groups ]

    obj_pending_users = obj_data.get("pending_users", [])
    obj_pending_groups = obj_data.get("pending_groups", [])
    
    pending_users = obj_pending_users or []
    pending_groups = obj_pending_groups or []
    pending_users_emails = [ i["user_email"] for i in pending_users ]
    pending_groups_ids = [ i["group_id"] for i in pending_groups ]

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
    msg_title = basic_invitation.pop("message_title", None)

    ### A/ parse invitees ###
    invitations = []
    for invitee in basic_invitation["invitees"] :
      print("\ninvite > invitee : ", invitee)

      ### - create invitations for invitee / user (if not invitor)
      if invitee["invitee_type"] == "user" :
        invitee_email = invitee["invitee_email"]
        invitee_id = invitee["invitee_id"]
        if invitor_email != invitee_email and invitee_email not in authorized_users_emails and invitee_email not in pending_users_emails:
          invitation = InvitationCreate(
            **basic_invitation,
            invitee = invitee_email,
            invitee_type = "user",
            invitee_id = invitee_id
          )
          print("invite > invitation : ", invitation)
          invitations.append(invitation)

      ### - create invitations for group
      if invitee["invitee_type"] == "group" :
        # get group's users & emails
        group_id = invitee["invitee_id"]

        # group_manage_level = group_in_db.manage
        # print("invite > group_manage_level : ", group_manage_level)

        ### invite group owner (if not invitor)
        if group_id not in authorized_groups_ids and group_id not in pending_groups_ids :
          group_in_db = db.query(Group).filter(Group.id == group_id).first()
          print("invite > group_in_db : ", group_in_db)

          group_owner_id = group_in_db.owner_id
          group_owner_in_db = db.query(User).filter(User.id == group_owner_id).first()
          print("invite > group_owner_in_db : ", group_owner_in_db)

          invitation = InvitationCreate(
            **basic_invitation,
            invitee = group_owner_in_db.email,
            invitee_type = "group",
            invitee_id = group_owner_in_db.id
          )
          invitations.append(invitation)

        # group_users = group_in_db.authorized_users
        # print("invite > group_users : ", group_users)


    ### - register and send invitations to invitees
    print("\ninvite > loop invitations ...")
    for invit in invitations :
      print("\ninvite > invit : ", invit)
      invit_data = jsonable_encoder(invit)
      print("invite > invit_data : ", invit_data)
      invitation_for_db = Invitation(
        **invit_data,
        owner_id = invitor_id
      )
      # print("invite > invitation_for_db - A : ", invitation_for_db)
      
      # save invitation in DB
      db.add(invitation_for_db)
      db.commit()
      db.refresh(invitation_for_db)
      # print("invite > invitation_for_db - B : ", invitation_for_db)
      print("invite > invitation_for_db.id : ", invitation_for_db.id )

      # update pending users list for object
      if invit_data["invitee_type"] == "user":
        pending_user = UserAuthPending(
          invitation_id = invitation_for_db.id,
          user_id = invit_data["invitee_id"],
          user_email = invit_data["invitee"],
        )
        pending_users.append(pending_user.dict())

      # update pending groups list for object
      if invit_data["invitee_type"] == "group":
        pending_group = GroupAuthPending(
          invitation_id = invitation_for_db.id,
          group_id = invit_data["invitee_id"]
        )
        pending_groups.append(pending_group.dict())

      invit_verify_token = generate_invit_token(email=invitation_for_db.invitee)
      # print("invite > invit_verify_token : ", invit_verify_token)

      # send invitation email
      background_tasks.add_task(
        send_invitation_email,
        email_from = invitor.email,
        name = invitor.name,
        surname = invitor.surname,
        username = invitor.username,
        token = invit_verify_token,
        invitation = invit_data
      )

    ### B/ update invitor data ###
    ### - send email to invitor resuming invitations sent
    # background_tasks.add_task(
    #   send_invitation_email,
    #   email_from = invitor.email,
    #   name = invitor.name,
    #   surname = invitor.surname,
    #   username = invitor.username,
    #   token = invit_verify_token,
    #   invitation = invit_data
    # )

    ### C/ update object ###
    ### - append every invitee as pending user / group

    print("\ninvite > pending_users B : ", pending_users)
    print("invite > pending_groups B : ", pending_groups)

    # pending_users = [ p.dict() for p in pending_users]
    # pending_groups = [ p.dict() for p in pending_groups]
    # print("\ninvite > pending_users B : ", pending_users)
    # print("invite > pending_groups B : ", pending_groups)

    # obj_data["pending_users"] = pending_users
    # if basic_invitation["invitation_to_item_type"] != "group" :
    #   obj_data["pending_groups"] = pending_groups
    # print("\ninvite > obj_data : ", obj_data)
    
    setattr(db_obj, "pending_users", pending_users)
    if basic_invitation["invitation_to_item_type"] != "group" :
      setattr(db_obj, "pending_groups", pending_groups)
    print("\ninvite > db_obj : ", db_obj)

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
