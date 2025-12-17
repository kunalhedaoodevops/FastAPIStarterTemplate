import strawberry
from typing import Optional

@strawberry.type
class Item:
    id: int
    title: str
    description: Optional[str]
    price: float
    owner_id: int
