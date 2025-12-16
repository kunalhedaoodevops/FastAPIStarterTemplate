import strawberry
from fastapi import HTTPException, status

from app.graphql.types.user import User
from app.graphql.inputs.user import UserCreateInput, UserUpdateInput
from app.services import Users_Service
from app.utils.deps import require_role

@strawberry.type
class UserMutation:

    @strawberry.mutation
    def create_user(self, info, data: UserCreateInput) -> User:
        db = info.context["db"]
        require_role("admin")(info.context["current_user"])

        existing = Users_Service.get_user_by_email(db, data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        return Users_Service.create_user(db, data)

    @strawberry.mutation
    def update_user(self, info, user_id: int, data: UserUpdateInput) -> User:
        db = info.context["db"]
        require_role("admin")(info.context["current_user"])

        user = Users_Service.get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return Users_Service.update_user(db, user, vars(data))

    @strawberry.mutation
    def delete_user(self, info, user_id: int) -> bool:
        db = info.context["db"]
        require_role("admin")(info.context["current_user"])

        user = Users_Service.get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        Users_Service.delete_user(db, user)
        return True
