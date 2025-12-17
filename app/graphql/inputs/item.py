import strawberry
from typing import Optional

@strawberry.input
class ItemCreateInput:
    title: str
    description: Optional[str] = None
    price: float

@strawberry.input
class ItemUpdateInput:
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
