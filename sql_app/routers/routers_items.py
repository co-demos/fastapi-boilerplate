# print(">>>>>> import routers.routers_items.py ...")

# from . import ( List, Session, APIRouter, Depends,
#   HTTPException, status,
#   get_db,
# )

# from ..schemas.schemas_item import Item, ItemCreate, ItemUpdate, ItemList
# from ..crud.crud_items import item

# from ..models.models_user import User
# from ..crud.crud_users import (
#   get_current_user,
#   get_current_user_optional,
# )


# router = APIRouter()


# @router.post(
#   "/",
#   summary="Create an item",
#   description="Create an item, including the id of the user creating the item",
#   response_model=Item,
#   status_code=status.HTTP_201_CREATED
# )
# def create_item_for_user(
#   item_in: ItemCreate,
#   db: Session = Depends(get_db),
#   current_user: User = Depends(get_current_user)
#   ):
#   user_id = current_user.id
#   return item.create_with_owner(db=db, obj_in=item_in, owner_id=user_id)


# @router.get(
#   "/{item_id}",
#   summary="Get an item",
#   description="Get an item by its id",
#   response_model=ItemList
#   )
# def read_item(item_id: int , db: Session = Depends(get_db)):
#   item_in_db = item.get_by_id(db, id=item_id, user=current_user, req_type="read" )
#   if item_in_db is None:
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
#   return item_in_db


# @router.get(
#   "/",
#   summary="Get a list of all items",
#   description="Get alll items given a limit",
#   response_model=List[Item]
# )
# def read_items(
#   skip: int = 0, limit: int = 100, 
#   db: Session = Depends(get_db)
#   ):
#   items = item.get_multi(db, skip=skip, limit=limit)
#   return items
