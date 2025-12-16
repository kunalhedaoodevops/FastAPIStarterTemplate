from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..databases import schemas
from ..databases.db import get_db
from . import security
from ..services import Users_Service
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = security.decode_access_token(token)
    if not payload or 'user_id' not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid authentication credentials')
    user = Users_Service.get_user(db, payload['user_id'])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user

def require_role(role: str):
    def role_checker(current_user: schemas.UserOut = Depends(get_current_user)):
        if current_user.role != role and current_user.role != 'admin':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Insufficient permissions')
        return current_user
    return role_checker