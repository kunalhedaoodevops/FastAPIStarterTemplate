from sqlalchemy.orm import Session
from ..models import files as files_models
from typing import Optional
from ..databases import schemas
from sqlalchemy import or_, func


# Files

def save_file_record(db: Session, filebase: schemas.FileCreate):
    db_file = files_models.FileStore(
        original_filename=filebase.original_filename,
        stored_filename=filebase.stored_filename,
        file_size=filebase.file_size,
        client_ip=filebase.client_ip,
        owner_id=filebase.owner_id
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def list_files(db: Session, current_user):
    query = db.query(files_models.FileStore).order_by(
        files_models.FileStore.uploaded_at.desc()
    )

    if current_user.role != "admin":
        query = query.filter(files_models.FileStore.owner_id == current_user.id)

    return query.all()

def get_file(db: Session, file_id: int) -> Optional[files_models.FileStore]:
    return db.query(files_models.FileStore).filter(files_models.FileStore.id == file_id).first()

def delete_file(db: Session, file_id: int):
    db_file = db.query(files_models.FileStore).filter(files_models.FileStore.id == file_id).first()
    if not db_file:
        return None
    # 2️⃣ Delete DB record
    db.delete(db_file)
    db.commit()

    return db_file

def download_file_by_id(db: Session, file_id: int):
    db_file = db.query(files_models.FileStore).filter(files_models.FileStore.id == file_id).first()
    return db_file

def download_file_by_filename(db: Session, filename: str):
    db_file = db.query(files_models.FileStore).filter(files_models.FileStore.original_filename == filename).first()
    return db_file.stored_filename

@staticmethod
def portable_search_file(
    db,
    q=None,
    min_size=None,
    max_size=None,
    uploaded_by=None,
    cursor=None,
    limit=20,
):
    query = db.query(files_models.FileStore)
    # 🔍 Portable prefix search
    if q:
        q = q.strip().lower()
        query = query.filter(
            or_(
                func.lower(files_models.FileStore.original_filename).startswith(q),
                func.lower(files_models.FileStore.stored_filename).startswith(q),
            )
        )
    # 📦 FileStore size filters
    if min_size is not None:
        query = query.filter(files_models.FileStore.file_size >= min_size)
    if max_size is not None:
        query = query.filter(files_models.FileStore.file_size <= max_size)
    # 👤 Uploaded by user (if column exists)
    if uploaded_by:
        query = query.filter(files_models.FileStore.user_id == uploaded_by)
    # Cursor pagination
    if cursor:
        query = query.filter(files_models.FileStore.id > cursor)
    return (
        query.order_by(files_models.FileStore.id)
        .limit(limit)
        .all()
    )