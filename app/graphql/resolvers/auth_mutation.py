import strawberry
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.graphql.types.auth import Token
from app.graphql.inputs.auth import LoginInput
from app.services import Users_Service
from app.utils import security
from app.core.config import settings
from app.utils.password_reset import create_reset_token, verify_reset_token
from app.utils.email import send_reset_email
from app.utils.security import get_password_hash
from app.graphql.types.auth import ForgotPasswordInput, ResetPasswordInput
from app.graphql.types.common import MessageResponse
from app.databases.db import get_db

@strawberry.type
class AuthMutation:

    @strawberry.mutation
    def login(self, info, data: LoginInput) -> Token:
        db = info.context["db"]

        user = Users_Service.get_user_by_email(db, data.username)
        if not user or not security.verify_password(
            data.password, user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        token = security.create_access_token(
            {"user_id": user.id, "role": user.role}
        )

        return Token(
            access_token=token,
            token_type="bearer",
        )
    @strawberry.mutation
    def forgot_password(
        self,
        info,
        data: ForgotPasswordInput,
    ) -> MessageResponse:
        db: Session = next(get_db())

        user = Users_Service.get_user_by_email(db, data.email)

        # 🔒 Do not reveal user existence
        if user:
            token = create_reset_token(user.email)
            reset_link = (
                f"{settings.FRONTEND_URL}/reset-password?token={token}"
            )
            send_reset_email(user.email, reset_link)

        return MessageResponse(
            message="If the email exists, a reset link has been sent"
        )

    @strawberry.mutation
    def reset_password(
        self,
        info,
        data: ResetPasswordInput,
    ) -> MessageResponse:
        db: Session = next(get_db())

        email = verify_reset_token(data.token)
        if not email:
            return MessageResponse(
                message="Invalid or expired token"
            )

        user = Users_Service.get_user_by_email(db, email)
        if not user:
            return MessageResponse(
                message="User not found"
            )

        user.hashed_password = get_password_hash(data.new_password)
        db.commit()

        return MessageResponse(
            message="Password updated successfully"
        )