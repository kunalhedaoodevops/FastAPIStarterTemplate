import strawberry
from fastapi import HTTPException, status

from app.graphql.types.auth import Token
from app.graphql.inputs.auth import LoginInput
from app.services import Users_Service
from app.utils import security

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
