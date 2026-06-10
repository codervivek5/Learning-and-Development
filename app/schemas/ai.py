from typing import List

from pydantic import BaseModel, Field


class AIObjectivesRequest(BaseModel):
    project_id: int = Field(..., description="Project identifier for logging or future persistence")
    content_source: str = Field(..., description="Source of the input content, e.g. raw_input or file")
    content: str = Field(..., description="Text or document content used to generate objectives")


class AIObjectivesResponse(BaseModel):
    objectives: List[str] = Field(..., description="Generated learning objectives")


class AIInteractivityRequest(BaseModel):
    project_id: int = Field(..., description="Project identifier for logging or future persistence")
    content_source: str = Field(..., description="Source of the input content, e.g. raw_input or file")
    content: str = Field(..., description="Text or document content used to generate interactivity suggestions")


class AIInteractivityResponse(BaseModel):
    suggestions: List[str] = Field(..., description="Generated interactivity suggestions")
