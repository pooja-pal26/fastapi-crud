from pydantic import BaseModel, EmailStr
from typing import Optional

# ---------- User Schemas ----------
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True


# ---------- Token Schema (login ke baad) ----------

class Token(BaseModel):
    access_token: str
    token_type: str


# ---------- Item Schemas ----------

class ItemCreate(BaseModel):
    title: str
    description: Optional[str] = None

class ItemOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    owner_id: int

    class Config:
        from_attributes = True
        