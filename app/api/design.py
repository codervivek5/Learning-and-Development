from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_current_organization_id
from app.db.session import get_db
from app.models.user import User
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
    organization_id: int = Depends(get_current_organization_id),
    current_user: User = Depends(get_current_user),
):
    project = await ProjectService.get_project(db, project_id, organization_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Project {project_id} not found or unauthorized for organization "
                f"{organization_id}."
            ),
        )

    analysis_record = await TrainingContentService.get_latest_phase_output(
        db=db,
        project_id=project_id,
        phase="analysis",
        organization_id=organization_id,
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
        organization_id=organization_id,
    )

    return design_output


@router.get("/{project_id}", response_model=DesignResponse)
async def get_design_output(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    organization_id: int = Depends(get_current_organization_id),
):
    record = await TrainingContentService.get_latest_phase_output(
        db=db,
        project_id=project_id,
        phase="design",
        organization_id=organization_id,
    )
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Design output not found for this project.",
        )

    return record.content
