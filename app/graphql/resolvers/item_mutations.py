import strawberry
from fastapi import HTTPException, status

from app.graphql.types.item import Item
from app.graphql.inputs.item import ItemCreateInput, ItemUpdateInput
from app.services import Items_Service

@strawberry.type
class ItemMutation:

    @strawberry.mutation
    def create_item(self, info, data: ItemCreateInput) -> Item:
        user = info.context["current_user"]
        if not user:
            raise HTTPException(status_code=401, detail="Not authenticated")

        db = info.context["db"]
        return Items_Service.create_item(
            db,
            owner_id=user.id,
            item=data,   # Strawberry input → service handles it
        )

    @strawberry.mutation
    def update_item(self, info, item_id: int, data: ItemUpdateInput) -> Item:
        user = info.context["current_user"]
        if not user:
            raise HTTPException(status_code=401, detail="Not authenticated")

        db = info.context["db"]
        item = Items_Service.get_item(db, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        if item.owner_id != user.id and user.role != "admin":
            raise HTTPException(status_code=403, detail="Not permitted")

        return Items_Service.update_item(db, item, vars(data))

    @strawberry.mutation
    def delete_item(self, info, item_id: int) -> bool:
        user = info.context["current_user"]
        if not user:
            raise HTTPException(status_code=401, detail="Not authenticated")

        db = info.context["db"]
        item = Items_Service.get_item(db, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        if item.owner_id != user.id and user.role != "admin":
            raise HTTPException(status_code=403, detail="Not permitted")

        Items_Service.delete_item(db, item)
        return True
