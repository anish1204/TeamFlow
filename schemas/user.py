from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    name: str
    role: str = "user"

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    role: Optional[str] = None

class UserBasicResponse(BaseModel):
    id: int
    username: str
    name: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    username: str

    

class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True