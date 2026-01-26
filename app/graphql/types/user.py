import strawberry
from typing import Optional

@strawberry.type
class User:
    id: int
    email: str
    full_name: Optional[str]
    role: str
    is_active: bool
