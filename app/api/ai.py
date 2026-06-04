from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_current_organization_id
from app.db.session import get_db
from app.models.user import User
from app.schemas.ai import (
    AIInteractivityResponse,
    AIInteractivityRequest,
    AIObjectivesResponse,
    AIObjectivesRequest,
)
from app.services.ai_service import AIService

router = APIRouter()
service = AIService()


@router.post(
    "/objectives/generate",
    response_model=AIObjectivesResponse,
    status_code=status.HTTP_200_OK,
)
async def generate_ai_objectives(
    project_id: int = Form(...),
    content_source: str = Form(...),
    content: str = Form(...),
    db: AsyncSession = Depends(get_db),
    organization_id: int = Depends(get_current_organization_id),
    current_user: User = Depends(get_current_user),
):
    try:
        return await service.generate_ai_objectives(
            project_id=project_id,
            content_source=content_source,
            content=content,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate objectives: {str(exc)}",
        ) from exc


@router.post(
    "/interactivity-suggestions/generate",
    response_model=AIInteractivityResponse,
    status_code=status.HTTP_200_OK,
)
async def generate_ai_interactivity(
    project_id: int = Form(...),
    content_source: str = Form(...),
    content: str = Form(...),
    db: AsyncSession = Depends(get_db),
    organization_id: int = Depends(get_current_organization_id),
    current_user: User = Depends(get_current_user),
):
    try:
        return await service.generate_ai_interactivity(
            project_id=project_id,
            content_source=content_source,
            content=content,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate interactivity suggestions: {str(exc)}",
        ) from exc
