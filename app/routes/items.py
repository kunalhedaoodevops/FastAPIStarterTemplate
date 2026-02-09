from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..databases import schemas
from ..models import items as item_models
from ..services import Items_Service
from ..databases.db import get_db
from ..utils.deps import get_current_user
from fastapi_cache.decorator import cache

router = APIRouter(prefix='/items', tags=['📦 Item Management APIs'])

@router.post('/', response_model=schemas.ItemOut, summary="Create Item", description="""Creates a new item associated with the authenticated user.
- Auth Required: ✅
- Input: Title, description, price
- Output: Created item
- Used For: Item creation""")
@cache(expire=30)
def create_item(item_in: schemas.ItemCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return Items_Service.create_item(db, owner_id=current_user.id, item=item_in)

@router.get('/count', response_model=int, summary="Items Count", description="""Returns a paginated list of items.
- Auth Required: ✅
- Output: Get All Items Count""")
@cache(expire=30)
def read_items_count( db: Session = Depends(get_db)):
    items = db.query(item_models.Item).count()
    return items

@router.get("/search", response_model=List[schemas.ItemOut], summary="Fast Item Search", description=""""Optimized search endpoint using cursor-based pagination for large datasets.
- Auth Required: ❌
- Query Params:
    * `q`, `min_price`, `max_price`
    * `owner_id`, `cursor`, `limit`
- Output: Matching items
- Used For: High-performance search""")
@cache(expire=10)
def fast_search_items(
    q: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    owner_id: Optional[int] = None,
    cursor: Optional[int] = None,
    limit: int = 20,
    db: Session = Depends(get_db),
    skip: int = 0,
):
    limit = min(limit, 100)

    return Items_Service.portable_search(
        db=db,
        q=q,
        min_price=min_price,
        max_price=max_price,
        owner_id=owner_id,
        cursor=cursor,
        limit=limit,
        skip=skip,  # Cursor-based pagination doesn't use skip
    )

@router.get('/{item_id}', response_model=schemas.ItemOut, summary="Get Item by ID", description="""Fetches item details by item ID.
- Auth Required: ❌
- Path Param: `item_id`
- Output: Item object
- Used For: Item detail view""")
@cache(expire=30)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = Items_Service.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    return db_item

@router.get('/', response_model=List[schemas.ItemOut], summary="List Items", description="""Returns a paginated list of items with optional filters.
- Auth Required: ❌
- Query Params:
    * `page`, `size`, `skip`
    * `search`
    * `min_price`, `max_price`
    * `owner_id`
- Output: Item list
- Used For: Browsing items""")
@cache(expire=30)
def list_items(skip: int = 0, size: int = 10, search: Optional[str] = None, min_price: Optional[float] = None, max_price: Optional[float] = None, owner_id: Optional[int] = None, db: Session = Depends(get_db)):
    # if page < 1: page = 1
    # skip = (page - 1) * size
    items, total = Items_Service.list_items(db, skip=skip, limit=size, search=search, min_price=min_price, max_price=max_price, owner_id=owner_id)
    return items

@router.patch('/{item_id}', response_model=schemas.ItemOut, summary="Update Item", description="""Updates an existing item’s fields.
- Auth Required: ✅
- Path Param: `item_id`
- Input: Partial item data
- Output: Updated item
- Used For: Item modification""")
def update_item(item_id: int, changes: schemas.ItemUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_item = Items_Service.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    if db_item.owner_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not permitted')
    return Items_Service.update_item(db, db_item, changes)

@router.delete('/{item_id}', status_code=204, summary="Delete Item", description="""Removes an item permanently.
- Auth Required: ✅
- Path Param: `item_id`
- Output: No content (204)
- Used For: Item deletion""")
def delete_item(item_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_item = Items_Service.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    if db_item.owner_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not permitted')
    Items_Service.delete_item(db, db_item)
    return None

