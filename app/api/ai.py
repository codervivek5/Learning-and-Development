from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header, Path
from sqlalchemy.ext.asyncio import AsyncSession

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
    request_data: AICurriculumRequest,
    project_id: int = Path(..., description="Project / training ID"),
    db: AsyncSession = Depends(get_db),
    organization_id: int = Header(..., alias="X-Organization-ID"),
    current_user: User = Depends(get_current_user),
):
    """
    Generate an immediate needs analysis report for a project workspace.
    Ensures multi-tenant security limits before passing context fields to the AI agent execution layer.
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
        return await ai_service.generate_needs_analysis(
            project_id=project_id,
            title=request_data.title,
            target_audience=request_data.target_audience,
            objectives=request_data.objectives,
            additional_context=request_data.additional_context,
        )
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
    request_data: AIObjectivesRequest,
    db: AsyncSession = Depends(get_db),
    organization_id: int = Header(..., alias="X-Organization-ID"),
    current_user: User = Depends(get_current_user),
):
    """
    Generate recommended learning objectives using structured JSON payload details.
    Matches properties mapped directly from the interactive metadata configuration tables.
    """
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
    request_data: AIInteractivityRequest,
    db: AsyncSession = Depends(get_db),
    organization_id: int = Header(..., alias="X-Organization-ID"),
    current_user: User = Depends(get_current_user),
):
    """
    Recommend interactive elements based on course content sources and custom textbook strings.
    """
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
    request_data: AIStoryboardRequest,
    db: AsyncSession = Depends(get_db),
    organization_id: int = Header(..., alias="X-Organization-ID"),
    current_user: User = Depends(get_current_user),
):
    """
    Generate storyboard slides built systematically from active design results.
    """
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