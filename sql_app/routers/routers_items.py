from . import ( List, Session, APIRouter, Depends,
  get_db,
  schemas_item, crud_items,
  models_user
)

from ..crud.crud_users import (
  get_current_user,
)

router = APIRouter()

@router.post("/", response_model=schemas_item.Item)
def create_item_for_user(
  item: schemas_item.ItemCreate,
  db: Session = Depends(get_db),
  current_user: models_user.User = Depends(get_current_user)
  ):
  user_id = current_user.id
  return crud_items.create_user_item(db=db, item=item, user_id=user_id)


@router.get("/{item_id}", response_model=schemas_item.ItemList)
def read_item(item_id: int , db: Session = Depends(get_db)):
  item = crud_items.get_item(db, id=item_id)
  return item


@router.get("/", response_model=List[schemas_item.Item])
def read_items(
  skip: int = 0, limit: int = 100, 
  db: Session = Depends(get_db)
  ):
  items = crud_items.get_items(db, skip=skip, limit=limit)
  return items
