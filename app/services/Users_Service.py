from sqlalchemy.orm import Session

from ..databases import schemas
from ..utils import security
from ..models import users

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
    for k, v in changes.dict(exclude_unset=True).items():
        setattr(db_user, k, v)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, db_user: users.User):
    db.delete(db_user)
    db.commit()
    return True
