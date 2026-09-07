from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    learning_level: str = "beginner"
    learning_style: str = "visual"


class UserUpdate(BaseModel):
    name: Optional[str] = None
    learning_level: Optional[str] = None
    learning_style: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    learning_level: str
    learning_style: str

    class Config:
        from_attributes = True