from fastapi import APIRouter, Depends, HTTPException, status, Header, Path, Form
from enum import Enum
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.services.project_service import ProjectService
from app.services.ai_service import AIService
from app.schemas.ai import (
    AICurriculumRequest,
    AIObjectivesRequest,
    AIObjectivesResponse,
    AIInteractivityRequest,
    AIInteractivityResponse,
    AIStoryboardRequest,
    AIStoryboardResponse,
)

router = APIRouter()

class ContentSourceType(str, Enum):
    RAW_INPUT = "raw_input"
    FILE = "file"
    DOCUMENT = "document"

async def verify_tenant_header(
        x_organization_id: int = Header(..., alias="X-Organization-ID", description="Active Tenant Organization ID")
):
    """Ensures X-Organization-ID is validated through HTTP Headers instead of Query Parameters."""
    return x_organization_id


@router.post(
    "/needs-analysis/{project_id}",
    response_model=dict,
    dependencies=[Depends(verify_tenant_header)]
)
async def generate_needs_analysis_direct(
        project_id: int = Path(..., description="Project ID"),
        title: str = Form(..., description="Title of the curriculum"),
        target_audience: str = Form(..., description="Target audience description"),
        objectives: List[str] = Form(..., description="List of learning objectives"),
        additional_context: Optional[str] = Form(None, description="Extra context"),
        db: AsyncSession = Depends(get_db),
        organization_id: int = Header(..., alias="X-Organization-ID"),
        current_user: User = Depends(get_current_user),
):
    """
    Generate an immediate needs analysis report using Form Data.
    """
    project = await ProjectService.get_project(
        db=db, project_id=project_id, organization_id=organization_id
    )
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or unauthorized access"
        )

    ai_service = AIService()
    try:
        # Create request object from form data to maintain consistency with service layer
        request_data = AICurriculumRequest(
            project_id=project_id,
            title=title,
            target_audience=target_audience,
            objectives=objectives,
            additional_context=additional_context
        )
        return await ai_service.generate_needs_analysis(request_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis agent execution failed: {str(e)}"
        )


@router.post(
    "/objectives/generate",
    response_model=AIObjectivesResponse,
    dependencies=[Depends(verify_tenant_header)]
)
async def generate_objectives(
        project_id: int = Form(..., description="Project ID"),
        content_source: ContentSourceType = Form(..., description="Content source type"),
        content: str = Form(..., description="Content body"),
        target_audience_description: Optional[str] = Form(None, description="Target audience description"),
        db: AsyncSession = Depends(get_db),
        organization_id: int = Header(..., alias="X-Organization-ID"),
        current_user: User = Depends(get_current_user),
):
    """
    Generate recommended learning objectives using structured Form Data payload.
    Matches properties mapped directly from the interactive metadata configuration tables.
    """
    # Create request object from form data to maintain consistency with service layer
    request_data = AIObjectivesRequest(
        project_id=project_id,
        content_source=content_source,
        content=content,
        target_audience_description=target_audience_description or ""
    )

    project = await ProjectService.get_project(
        db=db, project_id=request_data.project_id, organization_id=organization_id
    )
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or unauthorized access"
        )

    ai_service = AIService()
    try:
        return await ai_service.generate_objectives(request_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Objectives generation failed: {str(e)}"
        )


@router.post(
    "/interactivity-suggestions/generate",
    response_model=AIInteractivityResponse,
    dependencies=[Depends(verify_tenant_header)]
)
async def generate_interactivity_suggestions(
        project_id: int = Form(..., description="Project ID"),
        content_source: ContentSourceType = Form(..., description="Content source type"),
        content: str = Form(..., description="Content body"),
        db: AsyncSession = Depends(get_db),
        organization_id: int = Header(..., alias="X-Organization-ID"),
        current_user: User = Depends(get_current_user),
):
    """
    Recommend interactive elements based on course content sources and custom textbook strings using Form Data.
    """
    request_data = AIInteractivityRequest(project_id=project_id, content_source=content_source, content=content)

    project = await ProjectService.get_project(
        db=db, project_id=request_data.project_id, organization_id=organization_id
    )
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or unauthorized access"
        )

    ai_service = AIService()
    try:
        return await ai_service.generate_interactivity_suggestions(request_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Interactivity suggestions generation failed: {str(e)}"
        )


@router.post(
    "/storyboard/generate",
    response_model=AIStoryboardResponse,
    dependencies=[Depends(verify_tenant_header)]
)
async def generate_storyboard_slides(
        project_id: int = Form(..., description="Project ID"),
        topic_outline: str = Form(..., description="Topic outline"),
        learning_goals: List[str] = Form(..., description="List of learning goals"),
        db: AsyncSession = Depends(get_db),
        organization_id: int = Header(..., alias="X-Organization-ID"),
        current_user: User = Depends(get_current_user),
):
    """
    Generate storyboard slides built systematically from active design results using Form Data.
    """
    request_data = AIStoryboardRequest(project_id=project_id, topic_outline=topic_outline,
                                       learning_goals=learning_goals)

    project = await ProjectService.get_project(
        db=db, project_id=request_data.project_id, organization_id=organization_id
    )
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or unauthorized access"
        )

    ai_service = AIService()
    try:
        return await ai_service.generate_storyboard_slides(request_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Storyboard generation failed: {str(e)}"
        )