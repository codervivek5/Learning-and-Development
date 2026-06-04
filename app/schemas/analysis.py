from typing import List, Optional

from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    title: str = Field(..., description="Title of the course or learning project")
    target_audience: str = Field(..., description="Learner audience for this training")
    objectives: List[str] = Field(..., description="Baseline learning objectives for the project")
    additional_context: Optional[str] = Field(None, description="Optional business, compliance, or domain context")


class AnalysisOutput(BaseModel):
    learner_profile: str = Field(..., description="Learner profile and prerequisites summary")
    knowledge_gaps: List[str] = Field(..., description="Identified gaps in skills or knowledge")
    delivery_recommendations: str = Field(..., description="Recommended training delivery and modality")
    assessment_strategy: str = Field(..., description="Summary of assessment and evaluation methods")
    constraints_and_risks: Optional[str] = Field(None, description="Known constraints, dependencies, or risk factors")


class AnalysisResponse(BaseModel):
    phase: str = Field("analysis", description="Workflow phase name")
    output: AnalysisOutput = Field(..., description="Structured analysis output for the project")
