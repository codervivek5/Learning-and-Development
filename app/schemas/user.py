# app/schemas/user.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.core.constants import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: Optional[UserRole] = UserRole.LEARNER
    organization_id: Optional[int] = None
    organization_name: Optional[str] = None  # To support creating org on signup


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: UserRole
    organization_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
