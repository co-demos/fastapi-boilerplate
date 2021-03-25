from . import List, Session, APIRouter, Depends, \
  get_db, \
  schemas_item, crud_items

router = APIRouter()

@router.post("/", response_model=schemas_item.Item)
def create_item_for_user(
  item: schemas_item.ItemCreate, db: Session = Depends(get_db)
):
  return crud_items.create_user_item(db=db, item=item)


@router.get("/", response_model=List[schemas_item.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  items = crud_items.get_items(db, skip=skip, limit=limit)
  return items
