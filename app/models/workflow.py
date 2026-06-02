import uuid
from typing import Dict, Any, Optional
from sqlmodel import Field, Relationship, SQLModel, Column, JSON
from app.db.base import TimestampModel, TenantMixin
from app.core.constants import WorkflowPhase, WorkflowStatus


class WorkflowRun(TimestampModel, TenantMixin, table=True):
    """Execution state of ADDIE agents workflows."""

    __tablename__ = "workflow_run"

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        index=True,
        nullable=False,
    )
    project_id: int = Field(foreign_key="project.id", index=True, nullable=False)

    current_phase: WorkflowPhase = Field(default=WorkflowPhase.ANALYSIS, nullable=False)
    status: WorkflowStatus = Field(default=WorkflowStatus.PENDING, nullable=False)

    # State data containing intermediate and final generated materials (curriculum, storyboard)
    state_data: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    logs: Optional[str] = Field(default=None, max_length=5000)

    # Relationships
    project: "Project" = Relationship(back_populates="workflows")