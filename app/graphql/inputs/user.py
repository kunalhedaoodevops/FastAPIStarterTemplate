import strawberry
from typing import Optional

@strawberry.input
class UserCreateInput:
    email: str
    password: str
    full_name: Optional[str] = None
    role: str = "user"

@strawberry.input
class UserUpdateInput:
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
