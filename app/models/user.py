# app/model/user.py
from typing import Optional
from sqlmodel import Field
from app.db.base import TimestampModel
from app.core.constants import UserRole


class User(TimestampModel, table=True):
    """User accounts model."""

    __tablename__ = "user"

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        index=True,
        nullable=False,
    )
    email: str = Field(nullable=False, unique=True, index=True, max_length=255)
    hashed_password: str = Field(nullable=False)
    full_name: str = Field(nullable=False, max_length=255)
    role:str = Field(default=UserRole.LEARNER.value, nullable=False,max_length=100)
    is_active: bool = Field(default=True)

