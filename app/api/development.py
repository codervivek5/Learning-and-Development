from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, RoleChecker
from app.db.session import get_db
from app.models.user import User
from app.core.constants import UserRole
from app.schemas.development import DevelopmentResponse
from app.services.ai_service import AIService
from app.services.project_service import ProjectService
from app.services.training_content_service import TrainingContentService

router = APIRouter()
service = AIService()


@router.post("/{project_id}", response_model=DevelopmentResponse, status_code=status.HTTP_201_CREATED)
async def run_development_phase(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    # RBAC Guard: Restricting execution exclusively to platform ADMINS
    current_user: User = Depends(RoleChecker([UserRole.ADMIN])),
):
    """
    Execute the e-learning development phase to generate final learning scripts or raw course structures.
    Accessible only by users with Admin role privileges.
    """
    project = await ProjectService.get_project(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found.",
        )

    design_record = await TrainingContentService.get_latest_phase_output(
        db=db,
        project_id=project_id,
        phase="design",
    )
    if not design_record:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Design phase must be completed before development can run.",
        )

    development_output = await service.generate_development(
        project_id=project_id,
        design_results=design_record.content,
    )

    await TrainingContentService.save_phase_output(
        db=db,
        project_id=project_id,
        phase="develop",
        content=development_output.model_dump(),
    )

    return development_output


@router.get("/{project_id}", response_model=DevelopmentResponse)
async def get_development_output(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    # RBAC Guard: Both LEARNERS and ADMINS can read the developed components
    current_user: User = Depends(RoleChecker([UserRole.LEARNER, UserRole.ADMIN])),
):
    """
    Retrieve generated asset artifacts and text objects related to the course development engine.
    Accessible by both Admin and Learner platform roles.
    """
    record = await TrainingContentService.get_latest_phase_output(
        db=db,
        project_id=project_id,
        phase="develop",
    )
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Development output not found for this project.",
        )

    return record.content