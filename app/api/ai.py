from fastapi import APIRouter, Depends, Form, HTTPException, status
from app.api.deps import get_current_user, RoleChecker
from app.db.session import get_db
from app.models.user import User
from app.core.constants import UserRole
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
    # RBAC Guard: Restricting heavy AI generations exclusively to platform ADMINS
    current_user: User = Depends(RoleChecker([UserRole.ADMIN])),
):
    """
    Generate actionable e-learning behavioral objectives using LLM layers.
    Accessible only by users with Admin role permissions.
    """
    try:
        # Note: 'db' session parameter was removed as it is not consumed by the service method
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
    # RBAC Guard: Restricting heavy AI generations exclusively to platform ADMINS
    current_user: User = Depends(RoleChecker([UserRole.ADMIN])),
):
    """
    Generate contextual interactive element layouts and strategic blueprints via AI.
    Accessible only by users with Admin role permissions.
    """
    try:
        # Note: 'db' session parameter was removed as it is not consumed by the service method
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