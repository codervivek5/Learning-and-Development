# app/services/workflow_service.py

import asyncio
from typing import Any, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.workflow import WorkflowRun
from app.models.project import Project
from app.core.constants import WorkflowPhase, WorkflowStatus
from app.core.logging import get_logger

logger = get_logger(__name__)


class WorkflowService:
    """Service coordinates workflow runs and ADDIE stages transition."""

    @staticmethod
    async def create_workflow_run(
        db: AsyncSession, project_id: int
    ) -> WorkflowRun:
        db_workflow = WorkflowRun(
            project_id=project_id,
            current_phase=WorkflowPhase.ANALYSIS,
            status=WorkflowStatus.PENDING,
            state_data={},
        )
        db.add(db_workflow)
        await db.commit()
        await db.refresh(db_workflow)
        return db_workflow

    @staticmethod
    async def get_workflow_run(
        db: AsyncSession, workflow_id: int
    ) -> Optional[WorkflowRun]:
        result = await db.execute(
            select(WorkflowRun).where(
                WorkflowRun.id == workflow_id,
            )
        )
        return result.scalars().first()

    @staticmethod
    async def update_workflow_run(
        db: AsyncSession,
        workflow_id: int,
        current_phase: Optional[WorkflowPhase] = None,
        status: Optional[WorkflowStatus] = None,
        state_data: Optional[Dict[str, Any]] = None,
        logs: Optional[str] = None,
    ) -> Optional[WorkflowRun]:
        db_workflow = await WorkflowService.get_workflow_run(db, workflow_id)
        if not db_workflow:
            return None

        if current_phase:
            db_workflow.current_phase = current_phase
        if status:
            db_workflow.status = status
        if state_data is not None:
            # Merge dictionary updates if state_data already exists
            merged = dict(db_workflow.state_data or {})
            merged.update(state_data)
            db_workflow.state_data = merged
        if logs:
            db_workflow.logs = (db_workflow.logs or "") + f"\n{logs}"

        db.add(db_workflow)
        await db.commit()
        await db.refresh(db_workflow)
        return db_workflow

    @staticmethod
    async def start_workflow_execution(
        db: AsyncSession, workflow_id: int
    ) -> Optional[WorkflowRun]:
        """Trigger background execution of the workflow run."""
        db_workflow = await WorkflowService.get_workflow_run(db, workflow_id)
        if not db_workflow:
            return None

        # Update status to running
        db_workflow.status = WorkflowStatus.RUNNING
        db.add(db_workflow)
        await db.commit()
        await db.refresh(db_workflow)

        # Trigger background execution
        try:
            from app.tasks.ai_generation_task import _async_run_workflow
            asyncio.create_task(_async_run_workflow(
                workflow_id_str=str(workflow_id),
            ))
            logger.info("Successfully started Workflow execution task in background", workflow_id=workflow_id)
        except Exception as e:
            logger.error("Failed to start workflow task", workflow_id=workflow_id, error=str(e))
            db_workflow.status = WorkflowStatus.FAILED
            db_workflow.logs = f"Failed to dispatch run: {str(e)}"
            db.add(db_workflow)
            await db.commit()

        return db_workflow
