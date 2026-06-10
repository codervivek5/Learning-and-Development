# app/schemas/workflow.py
from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel
from app.core.constants import WorkflowPhase, WorkflowStatus


class WorkflowCreate(BaseModel):
    project_id: int


class WorkflowUpdate(BaseModel):
    current_phase: Optional[WorkflowPhase] = None
    status: Optional[WorkflowStatus] = None
    state_data: Optional[Dict[str, Any]] = None
    logs: Optional[str] = None


class WorkflowResponse(BaseModel):
    id: int
    project_id: int
    current_phase: WorkflowPhase
    status: WorkflowStatus
    state_data: Dict[str, Any]
    logs: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
