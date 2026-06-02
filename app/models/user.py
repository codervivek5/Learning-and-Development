import uuid
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from app.db.base import TimestampModel, TenantMixin
from app.core.constants import UserRole


class User(TimestampModel, TenantMixin, table=True):
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
    role: UserRole = Field(default=UserRole.LEARNER, nullable=False)
    is_active: bool = Field(default=True)

    # Relationships
    organization: "Organization" = Relationship(back_populates="users")
