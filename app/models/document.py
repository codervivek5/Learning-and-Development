# app/models/document.py
import uuid
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from app.db.base import TimestampModel, TenantMixin


class Document(TimestampModel, TenantMixin, table=True):
    """Uploaded PDFs/documents used as context for the AI."""

    __tablename__ = "document"

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        index=True,
        nullable=False,
    )
    project_id: int = Field(foreign_key="project.id", index=True, nullable=False)

    filename: str = Field(nullable=False, max_length=255)
    file_path: str = Field(nullable=False, max_length=1000)
    file_size: int = Field(nullable=False)
    mime_type: str = Field(nullable=False, max_length=100)

    # Ingestion status into vector store
    is_embedded: bool = Field(default=False)

    # Relationships
    project: "Project" = Relationship(back_populates="documents")