from calendar import c
from pydoc import cli
from sqlalchemy.orm import Session
from ..models import files as files_models
from typing import Optional
from ..databases import schemas


# Files

def save_file_record(db: Session, filebase: schemas.FileCreate):
    db_file = files_models.FileStore(
        original_filename=filebase.original_filename,
        stored_filename=filebase.stored_filename,
        file_size=filebase.file_size,
        client_ip=filebase.client_ip,
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def list_files(db: Session):
    return (
        db.query(files_models.FileStore)
        .order_by(files_models.FileStore.uploaded_at.desc())
        .all()
    )
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