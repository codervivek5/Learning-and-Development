from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.deps import get_current_user, RoleChecker
from app.models.user import User
from app.core.constants import UserRole
from app.services.workflow_service import WorkflowService
from app.schemas.workflow import WorkflowCreate, WorkflowResponse

router = APIRouter()


@router.post("/", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
async def create_workflow_run(
    workflow_in: WorkflowCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.ADMIN])),
):
    """Register a new ADDIE workflow execution run for a project."""
    return await WorkflowService.create_workflow_run(
        db=db,
        project_id=workflow_in.project_id,
    )


@router.post("/{workflow_id}/run", response_model=WorkflowResponse)
async def start_workflow_run(
    workflow_id: int,
    db: AsyncSession = Depends(get_db),
    # RBAC Guard: Only ADMINS have the permissions to execute agent routines
    current_user: User = Depends(RoleChecker([UserRole.ADMIN])),
):
    """Trigger background execution of the multi-agent workflow."""
    workflow = await WorkflowService.start_workflow_execution(
        db=db,
        workflow_id=workflow_id,
    )
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow run not found or unauthorized",
        )
    return workflow


@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow_status(
    workflow_id: int,
    db: AsyncSession = Depends(get_db),
    # RBAC Guard: Both LEARNERS and ADMINS can view background run metrics
    current_user: User = Depends(RoleChecker([UserRole.LEARNER, UserRole.ADMIN])),
):
    """Fetch status, current phase, logs, and generated content for a run."""
    workflow = await WorkflowService.get_workflow_run(
        db=db,
        workflow_id=workflow_id,
    )
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow run not found or unauthorized",
        )
    return workflow