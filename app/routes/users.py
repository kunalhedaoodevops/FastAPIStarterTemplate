from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..databases import schemas
from ..services import Users_Service
from ..databases.db import get_db
from ..utils.deps import get_current_user, require_role
from ..models import users as user_models
from fastapi_cache.decorator import cache

router = APIRouter(prefix='/users', tags=['👤 User Management APIs'])

@router.post('/', response_model=schemas.UserOut, summary="Create User", description="""Creates a new user account in the system with default or specified role.
- Auth Required: ✅
- Input: Email, password, full name, role
- Output: Created user object
- Used For: User registration (admin-controlled)""")
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db), current_user=Depends(require_role('admin'))):
    existing = Users_Service.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')
    return Users_Service.create_user(db, user_in)

@router.get('/', response_model=List[schemas.UserOut], summary="List Users", description="""Returns a paginated list of users.
- Auth Required: ✅
- Query Params: skip, limit
- Output: List of users
- Used For: Admin user management""")
@cache(expire=30)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user=Depends(require_role('admin'))):
    users = db.query(user_models.User).offset(skip).limit(limit).all()
    return users

@router.get("/search", response_model=List[schemas.UserOut], summary="Search Users", description="""Provides advanced filtering and searching of users.
- Auth Required: ✅
- Query Params:
    * `q` (search text)
    * `is_active`
    * `role`
    * `cursor`
    * `limit`
- Output: Filtered user list
- Used For: Large-scale user search""")
@cache(expire=10)
def search_users(
    q: str | None = None,
    role: str | None = None,
    is_active: bool | None = None,
    cursor: int | None = None,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    if q and len(q) < 2:
        raise HTTPException(
            status_code=400,
            detail="Search query must be at least 2 characters"
        )

    limit = min(limit, 50)

    return Users_Service.portable_search_user(
        db=db,
        q=q,
        role=role,
        is_active=is_active,
        cursor=cursor,
        limit=limit,
    )

@router.get('/me', response_model=schemas.UserOut, summary="Get Current User", description="""Returns details of the currently authenticated user.
- Auth Required: ✅
- Output: Logged-in user profile
- Used For: Profile display""")
@cache(expire=30)
def read_me(current_user = Depends(get_current_user)):
    return current_user

@router.get('/{user_id}', response_model=schemas.UserOut, summary="Get User by ID", description="""Fetches a specific user using their unique ID.
- Auth Required: ✅
- Path Param: `user_id`
- Output: User object
- Used For: Viewing user details""")
@cache(expire=30)
def read_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(require_role('admin'))):
    user = Users_Service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user

@router.patch('/{user_id}', response_model=schemas.UserOut, summary="Update User", description="""Updates selected user fields such as name, role, or activation status.
- Auth Required: ✅
- Path Param: `user_id`
- Input: Partial user data
- Output: Updated user object
- Used For: User administration""")
def update_user(user_id: int, changes: schemas.UserUpdate, db: Session = Depends(get_db), current_user=Depends(require_role('admin'))):
    user = Users_Service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return Users_Service.update_user(db, user, changes)

@router.delete('/{user_id}', status_code=204, summary="Delete User", description="""Deletes a user from the system.
- Auth Required: ✅
- Path Param: `user_id`
- Output: No content (204)
- Used For: Account removal""")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(require_role('admin'))):
    user = Users_Service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    Users_Service.delete_user(db, user)
    return None

