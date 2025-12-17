import strawberry
import uuid
from pathlib import Path
from fastapi import HTTPException

from strawberry.file_uploads import Upload
from app.graphql.types.file import File
from app.services import Files_Service
from app.databases import schemas

UPLOAD_DIR = Path("./app/static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@strawberry.type
class FileMutation:

    @strawberry.mutation
    async def upload_file(self, info, file: Upload) -> File:
        user = info.context["current_user"]
        if not user:
            raise HTTPException(401, "Not authenticated")

        if user.role not in ("admin", "user"):
            raise HTTPException(403, "Not permitted")

        if not file.filename:
            raise HTTPException(400, "No file provided")

        db = info.context["db"]
        request = info.context["request"]

        file_ext = Path(file.filename).suffix
        new_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = UPLOAD_DIR / new_filename

        # Write file to disk
        with file_path.open("wb") as buffer:
            buffer.write(await file.read())

        filedata = schemas.FileCreate(
            original_filename=file.filename,
            stored_filename=new_filename,
            file_size=file_path.stat().st_size,
            client_ip=request.client.host if request.client else None,
        )

        return Files_Service.save_file_record(db, filedata)

    @strawberry.mutation
    def delete_file(self, info, file_id: int) -> bool:
        user = info.context["current_user"]
        if not user:
            raise HTTPException(401, "Not authenticated")

        if user.role != "admin":
            raise HTTPException(403, "Not permitted")

        db = info.context["db"]
        db_file = Files_Service.delete_file(db, file_id)
        if not db_file:
            raise HTTPException(404, "File record not found")

        file_path = UPLOAD_DIR / db_file.stored_filename
        if file_path.exists():
            file_path.unlink()

        return True
