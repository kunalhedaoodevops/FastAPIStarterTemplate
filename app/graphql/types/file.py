import strawberry
from typing import Optional

@strawberry.type
class File:
    id: int
    original_filename: str
    stored_filename: str
    file_size: int
    client_ip: Optional[str]
