from sqlalchemy.orm import Session
from ..databases import schemas
from ..models import items as item_models
from typing import Optional

# Items

def create_item(db: Session, owner_id: int, item: schemas.ItemCreate):
    db_item = item_models.Item(**item.dict(), owner_id=owner_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_item(db: Session, item_id: int):
    return db.query(item_models.Item).filter(item_models.Item.id == item_id).first()

def update_item(db: Session, db_item: item_models.Item, changes: schemas.ItemUpdate):
    for k, v in changes.dict(exclude_unset=True).items():
        setattr(db_item, k, v)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, db_item: item_models.Item):
    db.delete(db_item)
    db.commit()
    return True

def list_items(db: Session, skip: int = 0, limit: int = 10, search: Optional[str] = None, min_price: Optional[float] = None, max_price: Optional[float] = None, owner_id: Optional[int] = None):
    q = db.query(item_models.Item)
    if search:
        q = q.filter(item_models.Item.title.ilike(f"%{search}%"))
    if min_price is not None:
        q = q.filter(item_models.Item.price >= min_price)
    if max_price is not None:
        q = q.filter(item_models.Item.price <= max_price)
    if owner_id is not None:
        q = q.filter(item_models.Item.owner_id == owner_id)
    total = q.count()
    items = q.offset(skip).limit(limit).all()
    return items, total