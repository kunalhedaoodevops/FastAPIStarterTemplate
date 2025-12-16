from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..databases import schemas
from ..services import Users_Service
from ..databases.db import get_db
from ..utils.deps import get_current_user, require_role
from ..models import users as user_models
from fastapi_cache.decorator import cache

router = APIRouter(prefix='/users', tags=['users'])

@router.post('/', response_model=schemas.UserOut)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db), current_user=Depends(require_role('admin'))):
    existing = Users_Service.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')
    return Users_Service.create_user(db, user_in)

@router.get('/', response_model=List[schemas.UserOut])
@cache(expire=30)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user=Depends(require_role('admin'))):
    users = db.query(user_models.User).offset(skip).limit(limit).all()
    return users

@router.get('/me', response_model=schemas.UserOut)
@cache(expire=30)
def read_me(current_user = Depends(get_current_user)):
    return current_user

@router.get('/{user_id}', response_model=schemas.UserOut)
@cache(expire=30)
def read_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(require_role('admin'))):
    user = Users_Service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user

@router.patch('/{user_id}', response_model=schemas.UserOut)
def update_user(user_id: int, changes: schemas.UserUpdate, db: Session = Depends(get_db), current_user=Depends(require_role('admin'))):
    user = Users_Service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return Users_Service.update_user(db, user, changes)

@router.delete('/{user_id}', status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(require_role('admin'))):
    user = Users_Service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    Users_Service.delete_user(db, user)
    return None
