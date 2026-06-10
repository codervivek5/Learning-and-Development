# app/db/base.py
from datetime import datetime, timezone
from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel


class TimestampModel(SQLModel):
    """
    Reusable timestamp mixin.
    Adds created_at and updated_at columns to models.
    """

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
        nullable=False,
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={
            "onupdate": lambda: datetime.now(timezone.utc)
        },
        nullable=False,
    )