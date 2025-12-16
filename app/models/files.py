from sqlalchemy import Column, Integer, String, BigInteger, DateTime
from .base import Base
from sqlalchemy.sql import func

class FileStore(Base):
    __tablename__ = "filestore"

    id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(String(255), nullable=False)
    stored_filename = Column(String(255), nullable=False, unique=True)
    file_size = Column(BigInteger, nullable=False)
    client_ip = Column(String(45))
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())