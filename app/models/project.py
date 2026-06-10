# app/models/project.py
from typing import Dict, Any, List, Optional
from sqlmodel import Field, Relationship, Column, JSON
from app.db.base import TimestampModel


class Project(TimestampModel, table=True):
    """Learning and Development design projects."""

    __tablename__ = "project"

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        index=True,
        nullable=False,
    )
    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)

    # Settings and details (e.g. target audience, learning goals)
    settings: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    # Relationships
    workflows: List["WorkflowRun"] = Relationship(back_populates="project")
    documents: List["Document"] = Relationship(back_populates="project")