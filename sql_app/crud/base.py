print(">>>>>> import crud.base.py ...")
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

import json

from fastapi import HTTPException, BackgroundTasks, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from sqlalchemy import and_, or_, not_, func, tuple_, text, cast
from sqlalchemy.orm import Session

from ..db.base_class import BaseCommons
from ..models.models_user import User
from ..models.models_group import Group
from ..models.models_invitation import Invitation

from ..schemas.schemas_choices import OperatorType, RequestType
from ..schemas.schemas_invitation import InvitationBasics, InvitationCreate
from ..schemas.schemas_comment import CommentBasics, CommentCreate
from ..schemas.schemas_patch import PatchBasics, PatchCreate
from ..schemas.schemas_auths import AuthInfos, UserAuthInfos, GroupAuthInfos, UserAuthPending, GroupAuthPending

from ..emails.emails import send_invitation_email

from ..security.jwt import generate_invit_token

ModelType = TypeVar("ModelType", bound=BaseCommons)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


### exceptions for special cases
AUTHS_EXCEPTIONS = {
  "invitations" : { 
    "user_field": "email", 
    "item_field": "invitee",
    "level_fields": [ "read", "response" ]
  },
  "users" : { 
    "user_field": "id", 
    "item_field": "id",
    "level_fields": [ "write", "manage" ]
  },
}


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
  def __init__(self, model: Type[ModelType]):
    """
    CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    **Parameters**

    * `model`: A SQLAlchemy model class
    * `schema`: A Pydantic model (schema) class
    """
    self.model = model
    self.tablename_singlar = model.__tablename__[:-1]
    self.tablename_plural = model.__tablename__


  ###  AUTH CHECK RELATED

  def get_user_groups(
    self, db: Session, *,
    current_user: User,
    ):
    user_id = current_user.id
    user_ref = { "user_email": current_user.email }
    # filter groups user is in authorized users
    groups_in_db = db.query(Group).filter( 
      or_(
        Group.owner_id == user_id,
        Group.authorized_users.contains([user_ref]),
      )
    )
    return groups_in_db.all()

  def check_user_auth(
    self, db: Session,
    item,
    current_user: User,
    level_field: str,
    auth_exception = None,
    ):
    
    print("\ncheck_user_auth > level_field : ", level_field)
    print(f"check_user_auth > current_user.id : {current_user.id} / current_user.email : {current_user.email} ")
    
    check = False

    item_owner_id = getattr( item, "owner_id", None )
    item_auth = getattr( item, level_field, None )

    item_authorized_users = getattr( item, "authorized_users", [] )
    item_authorized_groups = getattr( item, "authorized_groups", [] )
    # print("check_user_auth > item_authorized_users : ", item_authorized_users)
    # print("check_user_auth > item_authorized_groups : ", item_authorized_groups)
    
    print(f"check_user_auth > id : {item.id} / owner_id {item_owner_id} ")

    user_auth_level = False

    ### get item's authorized users list
    if item_authorized_users:
      user_in_authorized_users = list(filter(lambda user: user['user_email'] == current_user.email, item_authorized_users))
      # print("check_user_auth > user_in_authorized_users : ", user_in_authorized_users)
      if user_in_authorized_users:
        user_auths = user_in_authorized_users[0]["auths"]
        user_auth_level = user_auths.get(level_field, False)
    # print("check_user_auth > user_auth_level : ", user_auth_level)

    ### get item's authorized users list
    if item_authorized_groups:
      user_groups = self.get_user_groups( db=db, current_user=current_user )
      user_groups_ids = set([ group.id for group in user_groups ])
      print("check_user_auth > user_groups_ids : ", user_groups_ids)
      print("check_user_auth > item_authorized_groups : ", item_authorized_groups)
      authorized_group_ids = set([ group["group_id"] for group in item_authorized_groups ])
      authorized_groups_ids_for_user = user_groups_ids.intersection(authorized_group_ids)
      print("check_user_auth > authorized_groups_ids_for_user : ", authorized_groups_ids_for_user)

    ### compute check depending on item_auth level
    if item_auth and item_auth == "public":
      check = True
    
    elif item_auth and item_auth == "owner-only":
      check = item_owner_id == current_user.id
      # print("check_user_auth > item_owner_id : ", item_owner_id)
      # print("check_user_auth > current_user.id : ", current_user.id)
    
    elif item_auth and item_auth == "owner+groups":
      check = user_auth_level or item_owner_id == current_user.id
    
    elif item_auth and item_auth == "owner+groups+users":
      check = current_user != None
    
    else: # check in case item_auth is None => owner can do everything
      check = item_owner_id == current_user.id

    if auth_exception and not check:
      is_level = level_field in auth_exception["level_fields"]
      left_user = getattr( current_user, auth_exception["user_field"] )
      right_item = getattr( item, auth_exception["item_field"] )
      check = is_level and right_item == left_user

    print(f"check_user_auth > {level_field} > check : ", check)
    return check

  def check_user_auth_against_item(
    self, db: Session,
    item,
    tablename: str,
    current_user: User,
    req_type: Optional[RequestType] = "read",
    ):

    auth_check = None
    
    if item:
      # print("\ncheck_user_auth_against_item > req_type : ", req_type)
      # print("check_user_auth_against_item > current_user.__dict__ : ", current_user.__dict__)
      user_superuser = current_user.is_superuser
      # print("check_user_auth_against_item > user_superuser : ", user_superuser)
      
      if user_superuser :
        auth_check = True
      else :
        auth_exception = AUTHS_EXCEPTIONS.get(tablename,  None)
        # print("check_user_auth_against_item > auth_exception : ", auth_exception)
        auth_check = self.check_user_auth( db, item, current_user, req_type, auth_exception )

    print("\ncheck_user_auth_against_item > auth_check : ", auth_check)
    if not auth_check:
      raise HTTPException(status_code=400, detail=f"Not enough permissions to {req_type} on {tablename} table / item.id : {item.id}")
    return auth_check


  ### GET REQUESTS

  def get_by_id(
    self, db: Session, 
    id: Any,
    user: Optional[User] = None,
    get_auth_check: bool = True,
    req_type: Optional[RequestType] = "read"
    ) -> Optional[ModelType]:

    # print("\nget_by_id > self.model.__tablename__ :", self.model.__tablename__)
    result = db.query(self.model).filter(self.model.id == id).first()
    if result is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.tablename_singlar} not found")
    
    if get_auth_check :
      check_auth = self.check_user_auth_against_item(db, result, self.tablename_plural, user, req_type)
    
    return result

  # def get_by_title(
  #   self, db: Session,
  #   title: str,
  #   user: Optional[User] = None,
  #   get_auth_check: bool = True,
  #   req_type: Optional[RequestType] = "read"
  #   ) -> ModelType:
  #   result = db.query(self.model).filter(self.model.title == title).first()
  #   if result is None:
  #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.tablename_singlar} not found")
    
  #   if get_auth_check :
  #     check_auth = self.check_user_auth_against_item(db, result, self.tablename_plural, user, req_type)
    
  #   return result


  ### GET MULTI REQUESTS

  def get_multi(
    self, db: Session, *, 
    skip: int = 0,
    limit: int = 100,
    user: Optional[User] = None,
    req_type: Optional[RequestType] = "read"
    ) -> List[ModelType]:

    print("\nget_multi > user : ", user)
    print("get_multi > req_type : ", req_type)

    results = db.query(self.model)

    ### filter given user and item's auth level
    search_args = [
      self.model.read == "public",
    ]

    if user:

      # search items opened to users
      search_args.append(self.model.read == "owner+groups+users")

      # search user's items
      if self.tablename_singlar == "user" :
        search_args.append(self.model.id == user.id)

      else : 
        search_args.append(self.model.owner_id == user.id)
        # search items shared with user
        user_ref = { "user_email": user.email }
        search_args.append(self.model.authorized_users.contains([user_ref]))

        # search items shared with groups user is part of (if self.model has a authorized_groups attribute)
        if getattr(self.model, "authorized_groups", None):
          user_groups = self.get_user_groups( db=db, current_user=user )
          user_groups_ids = set([ group.id for group in user_groups ])
          user_groups_refs = [ {"group_id" : group_id } for group_id in user_groups_ids ]
          print("get_multi > user_groups_refs : ", user_groups_refs)
          for group_ref in user_groups_refs:
            search_args.append(self.model.authorized_groups.contains([group_ref]))

    results = results.filter( or_(*search_args) )

    results = (
      results.offset(skip)
      .limit(limit)
      .all()
    )

    return results

  def get_multi_by_owner(
    self, db: Session, *,
    owner_id: int,
    skip: int = 0,
    limit: int = 100,
    ) -> List[ModelType]:

    items_in_db = db.query(self.model).filter(self.model.owner_id == owner_id)

    if skip > 0 :
      items_in_db = items_in_db.offset(skip)
    if limit and limit > 0 :
      items_in_db = items_in_db.limit(limit)

    results = items_in_db.all()
    return results

  def get_multi_by_authorized_user(
    self, db: Session, *,
    user_id: int,
    user_email: str,
    skip: int = 0,
    limit: int = 100,
    group_ids: list = [],
    ) -> List[ModelType]:

    print("\nget_multi_by_authorized_user > user_id : ", user_id)
    print("get_multi_by_authorized_user > user_email : ", user_email)
    print("get_multi_by_authorized_user > group_ids : ", group_ids)
    user_ref = { "user_email": user_email }
    print("get_multi_by_authorized_user > user_ref : ", user_ref)
    
    items_in_db = db.query(self.model).filter(
      self.model.owner_id != user_id, 
      self.model.authorized_users.isnot(None),
    )
    print("get_multi_by_authorized_user > items_in_db.count() : ", items_in_db.count())
    for i in items_in_db.all() :
      print( f"... get_multi_by_authorized_user > {i.id} > i.authorized_users : ", i.authorized_users )
    
    # filter items user is in authorized users
    items_in_db = items_in_db.filter( 
      self.model.authorized_users.contains([user_ref])
    )
    print("\nget_multi_by_authorized_user > items_in_db : ", items_in_db)

    # filter items user is part of authorized groups
    # TO DO
    # items_in_db = items_in_db.filter( 
    #   self.model.authorized_users.contains([user_ref])
    # )

    if skip > 0 :
      items_in_db = items_in_db.offset(skip)
    if limit and limit > 0 :
      items_in_db = items_in_db.limit(limit)

    results = items_in_db.all()
    return results


  ### SEARCH REQUESTS

  def search_multi_by_fields(
    self, db: Session, *, 
    q: str,
    fields: List[str],
    # auth_level: str,
    skip: int = 0,
    limit: int = 100,
    operator: OperatorType = OperatorType.or_,
    user: Optional[User] = None,
    req_type: Optional[RequestType] = "read"
    ) -> List[ModelType]:
    
    print("\nsearch_multi_by_fields > q : ", q)
    # print("search_multi_by_fields > auth_level : ", auth_level)
    print("search_multi_by_fields > fields : ", fields)
    # print("search_multi_by_fields > self.model : ", self.model)
    # print("search_multi_by_fields > self.model.__dict__ : ", self.model.__dict__)

    print("search_multi_by_fields > user : ", user)
    print("search_multi_by_fields > req_type : ", req_type)

    db_query = db.query(self.model)

    search_args_user = []

    ### limit to public items if not user
    if not user:
      search_args_user.append( self.model.read == "public" )
    
    ### filter items if user
    else :
      search_args_user_temp = []

      # search items opened to users
      search_args_user_temp.append(self.model.read == "owner+groups+users")

      # search user's items
      if self.tablename_singlar == "user" :
        search_args_user_temp.append(self.model.id == user.id)
      
      else : 
        search_args_user_temp.append(self.model.owner_id == user.id)

        # search items shared with user
        user_ref = { "user_email": user.email }
        search_args_user_temp.append(self.model.authorized_users.contains([user_ref]))

        # search items shared with groups user is part of (if self.model has a authorized_groups attribute)
        if getattr(self.model, "authorized_groups", None):
          user_groups = self.get_user_groups( db=db, current_user=user )
          user_groups_ids = set([ group.id for group in user_groups ])
          user_groups_refs = [ {"group_id" : group_id } for group_id in user_groups_ids ]
          print("get_multi > user_groups_refs : ", user_groups_refs)
          for group_ref in user_groups_refs:
            search_args_user_temp.append(self.model.authorized_groups.contains([group_ref]))

        search_args_user.append( or_(*search_args_user_temp) )

    db_query = db_query.filter(*search_args_user)


    search_args = []

    # parse query 
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

    print("search_multi_by_fields > results - end : ", results)
    return results, results_count


  ### CREATE REQUESTS

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


  ### UPDATE REQUESTS

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


  ### INVITE REQUESTS

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


  ### COMMENT / PATCH REQUESTS

  # def comment_or_patch(
  #   self, db: Session, *,
  #   db_obj: ModelType,
  #   background_tasks: BackgroundTasks,
  #   obj_in: [CommentBasics, PatchBasics],
  #   ) -> ModelType:
  #   print("\ncomment > db_obj : ", db_obj)
  #   print("comment > obj_in : ", obj_in)


  ### DELETE REQUESTS

  def remove(
    self, db: Session, *,
    id: int,
    current_user: User,
    ) -> ModelType:
    print("remove > id : ", id)
    print("remove > current_user.id : ", current_user.id)
    obj = db.query(self.model).get(id)
    if not obj:
      # raise HTTPException(status_code=404, detail="object not found")
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.tablename_singlar} not found")
    
    ### check auth to delete
    check_auth = self.check_user_auth_against_item(db, obj, self.tablename_plural, current_user, "manage")

    ### delete object
    db.delete(obj)

    ### delete corresponding invitations
    related_invitations = db.query(Invitation).filter(
      and_(
        Invitation.invitation_to_item_type == self.tablename_singlar,
        Invitation.invitation_to_item_id == id,
      )
    ).delete()
    # for invit in related_invitations.all() :
    #   db.delete(invit)
    print("remove > related_invitations : ", related_invitations)

    ### update related items (e.g. delete a dataset referenced in a workspace)
    ### TO DO 

    db.commit()
    return obj
