from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user, RoleChecker
from app.db.session import get_db
from app.models.user import User
from app.core.constants import UserRole
from app.schemas.review import ReviewResponse
from app.services.ai_service import AIService
from app.services.project_service import ProjectService
from app.services.training_content_service import TrainingContentService

router = APIRouter()
service = AIService()


@router.post("/{project_id}", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def run_review_phase(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    # RBAC Guard: Restricting execution exclusively to platform ADMINS
    current_user: User = Depends(RoleChecker([UserRole.ADMIN])),
):
    """
    Execute the e-learning review phase to evaluate the quality and depth of developed course content.
    Accessible only by users with Admin role privileges.
    """
    project = await ProjectService.get_project(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found.",
        )

    development_record = await TrainingContentService.get_latest_phase_output(
        db=db,
        project_id=project_id,
        phase="develop",
    )
    if not development_record:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Development phase must be completed before review can run.",
        )

    review_output = await service.generate_review(
        project_id=project_id,
        developed_content=development_record.content,
    )

    await TrainingContentService.save_phase_output(
        db=db,
        project_id=project_id,
        phase="review",
        content=review_output.model_dump(),
    )

    return review_output


@router.get("/{project_id}", response_model=ReviewResponse)
async def get_review_output(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    # RBAC Guard: Both LEARNERS and ADMINS can read the review metrics
    current_user: User = Depends(RoleChecker([UserRole.LEARNER, UserRole.ADMIN])),
):
    """
    Retrieve generated assessment reviews and compliance outputs for a project.
    Accessible by both Admin and Learner platform roles.
    """
    record = await TrainingContentService.get_latest_phase_output(
        db=db,
        project_id=project_id,
        phase="review",
    )
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review output not found for this project.",
        )

    return record.content