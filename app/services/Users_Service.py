from sqlalchemy.orm import Session
from ..databases import schemas
from ..utils import security
from ..models import users
from sqlalchemy import or_, func
# Users

def get_user(db: Session, user_id: int):
    return db.query(users.User).filter(users.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(users.User).filter(users.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed = security.get_password_hash(user.password)
    db_user = users.User(email=user.email, full_name=user.full_name, hashed_password=hashed, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: users.User, changes: schemas.UserUpdate):
    # ✅ Handle Pydantic OR dict
    if hasattr(changes, "dict"):
        changes = changes.dict(exclude_unset=True)

    # ✅ Ignore None values (VERY IMPORTANT)
    for k, v in changes.items():
        if v is not None:
            setattr(db_user, k, v)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, db_user: users.User):
    db.delete(db_user)
    db.commit()
    return True

@staticmethod
def portable_search_user(
    db,
    q=None,
    role=None,
    is_active=None,
    cursor=None,
    limit=20,
):
    query = db.query(users.User)
    # 🔍 Portable search (prefix-based)
    if q:
        q = q.strip().lower()
        query = query.filter(
            or_(
                func.lower(users.User.full_name).startswith(q),
                func.lower(users.User.email).startswith(q),
            )
        )
    # Filters
    if role:
        query = query.filter(users.User.role == role)
    if is_active is not None:
        query = query.filter(users.User.is_active == is_active)
    # Cursor pagination
    if cursor:
        query = query.filter(users.User.id > cursor)
    return (
        query.order_by(users.User.id)
        .limit(limit)
        .all()
    )