import uuid
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from app.db.base import TimestampModel


class Organization(TimestampModel, table=True):
    """Tenant Organization model."""

    __tablename__ = "organization"

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        index=True,
        nullable=False,
    )
    name: str = Field(nullable=False, max_length=255)
    slug: str = Field(nullable=False, unique=True, index=True, max_length=255)
    domain: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = Field(default=True)

    # Relationships
    users: List["User"] = Relationship(back_populates="organization")
    projects: List["Project"] = Relationship(back_populates="organization")