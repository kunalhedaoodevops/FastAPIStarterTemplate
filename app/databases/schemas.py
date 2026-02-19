from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[str] = None

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role: Optional[str] = 'user'

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None

class UserOut(UserBase):
    id: int
    is_active: bool
    role: str
    class Config:
        from_attributes = True

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float = 0

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

class ItemOut(ItemBase):
    id: int
    owner_id: int
    class Config:
        from_attributes = True

# 🔸 Input schema (CREATE)
class FileCreate(BaseModel):
    original_filename: str
    stored_filename: str
    file_size: int
    client_ip: str | None = None
    owner_id: int


# 🔸 Output schema (READ)
class FileOut(BaseModel):
    id: int
    original_filename: str
    stored_filename: str
    file_size: int
    client_ip: str | None
    uploaded_at: datetime
    owner_id: int
    model_config = ConfigDict(from_attributes=True)

class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str