import strawberry
from typing import List
from fastapi import HTTPException

from app.graphql.types.file import File
from app.services import Files_Service

@strawberry.type
class FileQuery:

    @strawberry.field
    def files(self, info) -> List[File]:
        user = info.context["current_user"]
        if not user:
            raise HTTPException(401, "Not authenticated")

        if user.role not in ("admin", "user"):
            raise HTTPException(403, "Not permitted")

        db = info.context["db"]
        return Files_Service.list_files(db)

    @strawberry.field
    def file(self, info, file_id: int) -> File:
        user = info.context["current_user"]
        if not user:
            raise HTTPException(401, "Not authenticated")

        if user.role not in ("admin", "user"):
            raise HTTPException(403, "Not permitted")

        db = info.context["db"]
        file_item = Files_Service.get_file(db, file_id)
        if not file_item:
            raise HTTPException(404, "File not found")

        return file_item
