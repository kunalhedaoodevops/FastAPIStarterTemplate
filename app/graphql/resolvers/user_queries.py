import strawberry
from typing import List, Optional
from fastapi import HTTPException

from app.graphql.types.user import User
from app.services import Users_Service
from app.utils.deps import require_role_graphql
from app.models import users as user_models

@strawberry.type
class UserQuery:

    @strawberry.field
    def users(self, info, skip: int = 0, limit: int = 100) -> List[User]:
        db = info.context["db"]
        require_role_graphql("admin")(info.context["current_user"])

        return (
            db.query(user_models.User)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @strawberry.field
    def user(self, info, user_id: int) -> Optional[User]:
        db = info.context["db"]
        require_role_graphql("admin")(info.context["current_user"])

        user = Users_Service.get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @strawberry.field
    def me(self, info) -> User:
        user = info.context["current_user"]
        if not user:
            raise HTTPException(status_code=401, detail="Not authenticated")
        return user
