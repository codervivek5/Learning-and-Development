from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, RoleChecker  # Fixed imports
from app.db.session import get_db
from app.models.user import User
from app.core.constants import UserRole
from app.schemas.analysis import AnalysisRequest, AnalysisOutput, AnalysisResponse
from app.services.ai_service import AIService
from app.services.project_service import ProjectService
from app.services.training_content_service import TrainingContentService

router = APIRouter()
service = AIService()


@router.post("/{project_id}", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
async def run_analysis(
    project_id: int,
    request: AnalysisRequest,
    db: AsyncSession = Depends(get_db),
    # RBAC Guard: Only ADMIN can trigger the analysis run
    current_user: User = Depends(RoleChecker([UserRole.ADMIN])),
):
    project = await ProjectService.get_project(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found.",
        )

    analysis_response = await service.generate_needs_analysis(
        project_id=project_id,
        request=request,
        db=db,
        user_id=current_user.id,
    )

    # Removed organization_id parameter from service call
    await TrainingContentService.save_phase_output(
        db=db,
        project_id=project_id,
        phase="analysis",
        content=analysis_response.output.model_dump(),
    )

    return analysis_response


@router.get("/{project_id}", response_model=AnalysisResponse)
async def get_analysis_output(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    # RBAC Guard: Both LEARNER and ADMIN can view the analysis results
    current_user: User = Depends(RoleChecker([UserRole.LEARNER, UserRole.ADMIN])),
):
    # Removed organization_id parameter from service call
    record = await TrainingContentService.get_latest_phase_output(
        db=db,
        project_id=project_id,
        phase="analysis",
    )
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis output not found for this project.",
        )

    content = record.content
    if isinstance(content, dict) and "output" in content:
        return AnalysisResponse.model_validate(content)

    return AnalysisResponse(phase="analysis", output=AnalysisOutput.model_validate(content))