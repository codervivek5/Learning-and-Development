from typing import Optional, Dict, Any

from sqlmodel import Field, SQLModel, Column, JSON

from app.db.base import TimestampModel, TenantMixin


class TrainingContent(TimestampModel, TenantMixin, table=True):
    __tablename__ = "training_content"

    id: Optional[int] = Field(default=None, primary_key=True)

    project_id: int = Field(
        foreign_key="project.id",
        index=True
    )

    phase: str = Field(
        index=True
    )

    content: Dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column(JSON)
    )