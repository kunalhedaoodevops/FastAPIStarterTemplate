from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session

from ..databases import schemas
from ..utils import security
from ..databases.db import get_db
from ..services import Users_Service
from app.utils.password_reset import verify_reset_token, create_reset_token
from app.utils.email import send_reset_email
from app.utils.security import get_password_hash
from app.core.config import settings

router = APIRouter(prefix='/auth', tags=['🔐 Authentication APIs'])

class SimpleLoginForm:
    def __init__(self, username: str = Form(...), password: str = Form(...)):
        self.username = username
        self.password = password


@router.post('/token', response_model=schemas.Token, summary="Login & Generate Access Token", description="""Authenticates a user using email/username and password.
On successful authentication, returns a JWT access token which must be used to access protected APIs.
- Auth Required: ❌
- Input: `username`, `password` (form data)
- Output: JWT access token
- Used For: Login, session authentication""")
def login_for_token(form_data: SimpleLoginForm = Depends(), db: Session = Depends(get_db)):
    user = Users_Service.get_user_by_email(db, form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')
    token = security.create_access_token({'user_id': user.id, 'role': user.role})
    return {'access_token': token, 'token_type': 'bearer'}

@router.post("/forgot-password", summary="Request Password Reset", description="""Initiates the password recovery process by accepting the user’s email address.
Typically sends a password reset token via email.
- Auth Required: ❌
- Input: Email address
- Output: Success acknowledgment
- Used For: Account recovery""")
def forgot_password(
    payload: schemas.ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    user = Users_Service.get_user_by_email(db, payload.email)

    # Do NOT reveal if user exists
    if user:
        token = create_reset_token(user.email)
        frontend = settings.FRONTEND_URL
        reset_link = f"{frontend}/reset-password?token={token}"
        send_reset_email(user.email, reset_link)

    return {"message": "If the email exists, a reset link has been sent"}

@router.post("/reset-password", summary="Reset User Password", description="""Resets the user password using a valid reset token generated from the forgot-password flow.
- Auth Required: ❌
- Input: Reset token, new password
- Output: Success acknowledgment
- Used For: Completing password reset""")
def reset_password(
    payload: schemas.ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    email = verify_reset_token(payload.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = Users_Service.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = get_password_hash(payload.new_password)
    db.commit()

    return {"message": "Password updated successfully"}
