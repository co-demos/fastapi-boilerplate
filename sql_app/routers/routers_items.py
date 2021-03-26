from . import ( List, Session, APIRouter, Depends,
  HTTPException, status,
  get_db,
  schemas_item, crud_items,
  models_user
)

from ..crud.crud_users import (
  get_current_user,
)


router = APIRouter()


@router.post(
  "/",
  summary="Create an item",
  description="Create an item, including the id of the user creating the item",
  response_model=schemas_item.Item,
  status_code=status.HTTP_201_CREATED
)
def create_item_for_user(
  item: schemas_item.ItemCreate,
  db: Session = Depends(get_db),
  current_user: models_user.User = Depends(get_current_user)
  ):
  user_id = current_user.id
  return crud_items.create_user_item(db=db, item=item, user_id=user_id)


@router.get(
  "/{item_id}",
  summary="Get an item",
  description="Get an item by its id",
  response_model=schemas_item.ItemList
  )
def read_item(item_id: int , db: Session = Depends(get_db)):
  item = crud_items.get_item(db, id=item_id)
  if item is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
  return item


@router.get(
  "/",
  summary="Get a list of all items",
  description="Get alll items given a limit",
  response_model=List[schemas_item.Item]
)
def read_items(
  skip: int = 0, limit: int = 100, 
  db: Session = Depends(get_db)
  ):
  items = crud_items.get_items(db, skip=skip, limit=limit)
  return items
