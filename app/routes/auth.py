from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session

from ..databases import schemas
from ..utils import security
from ..databases.db import get_db
from ..services import Users_Service
router = APIRouter(prefix='/auth', tags=['auth'])

class SimpleLoginForm:
    def __init__(self, username: str = Form(...), password: str = Form(...)):
        self.username = username
        self.password = password


@router.post('/token', response_model=schemas.Token)
def login_for_token(form_data: SimpleLoginForm = Depends(), db: Session = Depends(get_db)):
    user = Users_Service.get_user_by_email(db, form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')
    token = security.create_access_token({'user_id': user.id, 'role': user.role})
    return {'access_token': token, 'token_type': 'bearer'}