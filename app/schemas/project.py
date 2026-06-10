# app/schemas/project.py
from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel


class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class ProjectResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    settings: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
