import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import DateTime


class TimestampModel(SQLModel):
    """Mixin for created and updated timestamps."""

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
        nullable=False,
    )


class TenantMixin(SQLModel):
    """Mixin to segregate database tables by organization tenant."""

    organization_id: int = Field(
        foreign_key="organization.id",
        index=True,
        nullable=False,
    )
