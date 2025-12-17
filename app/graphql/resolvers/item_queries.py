import strawberry
from typing import List, Optional
from fastapi import HTTPException

from app.graphql.types.item import Item
from app.services import Items_Service

@strawberry.type
class ItemQuery:

    @strawberry.field
    def item(self, info, item_id: int) -> Item:
        db = info.context["db"]
        item = Items_Service.get_item(db, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

    @strawberry.field
    def items(
        self,
        info,
        page: int = 1,
        size: int = 10,
        search: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        owner_id: Optional[int] = None,
    ) -> List[Item]:
        if page < 1:
            page = 1

        db = info.context["db"]
        skip = (page - 1) * size

        items, total = Items_Service.list_items(
            db,
            skip=skip,
            limit=size,
            search=search,
            min_price=min_price,
            max_price=max_price,
            owner_id=owner_id,
        )
        return items
