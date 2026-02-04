from app.databases import schemas
from sqlalchemy.orm import Session
from ..databases.db import get_db
from ..utils.deps import get_current_user
from ..services import Files_Service
from fastapi import APIRouter, Request, UploadFile, File, HTTPException, Depends, status
from fastapi.responses import FileResponse
from pathlib import Path
import uuid
from typing import List
from fastapi_cache.decorator import cache

router = APIRouter(prefix='/files', tags=['📁 File Management APIs'])

UPLOAD_DIR = Path("./app/static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload", summary="Upload File", response_model=schemas.FileOut, description="""Uploads a file and stores its metadata.
- Auth Required: ✅
- Input: Multipart file
- Output: File metadata
- Used For: File storage""")
async def upload_file( request: Request, db: Session = Depends(get_db), file: UploadFile = File(...), current_user=Depends(get_current_user)):
    if current_user.role != 'admin' and current_user.role != 'user':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not permitted')

    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    # Create unique filename
    file_ext = Path(file.filename).suffix
    new_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / new_filename

    with file_path.open("wb") as buffer:
        buffer.write(await file.read())
    filedata = schemas.FileCreate(
        original_filename=file.filename,
        stored_filename=new_filename,
        file_size=file_path.stat().st_size,
        client_ip=request.client.host if request.client else None,
    )
    # Save file record to database
    return Files_Service.save_file_record(db,filedata)

@router.get("/search", response_model=List[schemas.FileOut], summary="Search Files", description="""Searches files using size, name, uploader, or cursor pagination.
- Auth Required: ✅
- Query Params:
    * `q`, `min_size`, `max_size`
    * `uploaded_by`, `cursor`, `limit`
- Output: Matching files
- Used For: File discovery""")
def search_files(
    q: str | None = None,
    min_size: int | None = None,
    max_size: int | None = None,
    uploaded_by: int | None = None,
    cursor: int | None = None,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role not in ("admin", "user"):
        raise HTTPException(status_code=403, detail="Not permitted")

    if q and len(q) < 2:
        raise HTTPException(
            status_code=400,
            detail="Search query must be at least 2 characters",
        )

    limit = min(limit, 50)

    return Files_Service.portable_search_file(
        db=db,
        q=q,
        min_size=min_size,
        max_size=max_size,
        uploaded_by=uploaded_by,
        cursor=cursor,
        limit=limit,
    )

@router.get("/download", summary="Download File", description="""Downloads a file using file ID or filename.
- Auth Required: ✅
- Query Params: `file_id` or `filename`
- Output: File stream
- Used For: File retrieval""")
def download_file(
    file_id: int | None = None,
    filename: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != 'admin' and current_user.role != 'user':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not permitted')

    if not file_id and not filename:
        raise HTTPException(400, "Provide file_id or filename")

    if file_id:
        db_file = Files_Service.download_file_by_id(db, file_id)
        if not db_file:
            raise HTTPException(404, "File not found")
        stored_filename = db_file.stored_filename
        download_name = db_file.original_filename

    elif filename:
        stored_filename = Files_Service.download_file_by_filename(db, filename)
        if not stored_filename:
            raise HTTPException(404, "File not found")
        download_name = filename

    else:
        stored_filename = filename
        download_name = filename

    file_path = UPLOAD_DIR / stored_filename

    if not file_path.exists():
        raise HTTPException(404, "File not found")

    return FileResponse(
        path=file_path,
        filename=download_name,
        media_type="application/octet-stream",
    )

@router.get(
    "/",
    response_model=List[schemas.FileOut],
    summary="List Files",
    description="""Returns all uploaded files accessible to the user.
    - Auth Required: ✅
    - Output: List of files
    - Used For: File browsing"""
)
@cache(expire=30)
def get_files(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != 'admin' and current_user.role != 'user':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not permitted')

    return Files_Service.list_files(db)

@router.get('/{file_id}', response_model=schemas.FileOut, summary="Get File Metadata", description="""Returns metadata information of a specific file.
- Auth Required: ✅
- Path Param: `file_id`
- Output: File metadata
- Used For: File inspection""")
@cache(expire=30)
def read_file(file_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != 'admin' and current_user.role != 'user':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not permitted')

    file_item = Files_Service.get_file(db, file_id)
    if not file_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='File not found')
    return file_item

@router.delete(
    "/{file_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete File",
    description="""Deletes a file and its metadata.
    - Auth Required: ✅
    - Path Param: `file_id`
    - Output: Success acknowledgment
    - Used For: File cleanup"""
)
def remove_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not permitted",
        )
    db_file = Files_Service.delete_file(db, file_id)
    if not db_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File record not found",
        )

    file_path = UPLOAD_DIR / db_file.stored_filename

    # 1️⃣ Delete file from disk (if exists)
    if file_path.exists():
        file_path.unlink()

    return {"message": "File deleted successfully"}