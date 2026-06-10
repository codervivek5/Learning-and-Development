from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, RoleChecker
from app.db.session import get_db
from app.models.user import User
from app.core.constants import UserRole
from app.schemas.design import DesignResponse
from app.services.ai_service import AIService
from app.services.project_service import ProjectService
from app.services.training_content_service import TrainingContentService

router = APIRouter()
service = AIService()


@router.post("/{project_id}", response_model=DesignResponse, status_code=status.HTTP_201_CREATED)
async def run_design_phase(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    # RBAC Guard: Restricting phase execution to platform ADMINS
    current_user: User = Depends(RoleChecker([UserRole.ADMIN])),
):
    """
    Execute the e-learning curriculum design blueprint process using past analysis data.
    Accessible only by users with Admin role permissions.
    """
    project = await ProjectService.get_project(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found.",
        )

    analysis_record = await TrainingContentService.get_latest_phase_output(
        db=db,
        project_id=project_id,
        phase="analysis",
    )
    if not analysis_record:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Analysis phase must be completed before design can run.",
        )

    analysis_results = analysis_record.content
    if isinstance(analysis_results, dict) and "output" in analysis_results:
        analysis_results = analysis_results["output"]

    design_output = await service.generate_design(
        project_id=project_id,
        analysis_results=analysis_results,
    )

    await TrainingContentService.save_phase_output(
        db=db,
        project_id=project_id,
        phase="design",
        content=design_output.model_dump(),
    )

    return design_output


@router.get("/{project_id}", response_model=DesignResponse)
async def get_design_output(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    # RBAC Guard: Both LEARNERS and ADMINS can read design metrics
    current_user: User = Depends(RoleChecker([UserRole.LEARNER, UserRole.ADMIN])),
):
    """
    Retrieve generated curriculum design frameworks and storyboards for a project.
    Accessible by both Admin and Learner platform roles.
    """
    record = await TrainingContentService.get_latest_phase_output(
        db=db,
        project_id=project_id,
        phase="design",
    )
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Design output not found for this project.",
        )

    return record.content