import asyncio
import uuid
from app.tasks.celery_app import celery_app
from app.core.database import AsyncSessionLocal
from app.models.workflow import WorkflowRun
from app.models.project import Project
from app.core.constants import WorkflowPhase, WorkflowStatus
from app.services.ai_service import AIService
from app.core.logging import get_logger

logger = get_logger(__name__)


async def _async_run_workflow(workflow_id_str: str, organization_id_str: str) -> None:
    workflow_id = uuid.UUID(workflow_id_str)
    organization_id = uuid.UUID(organization_id_str)

    ai_service = AIService()

    async with AsyncSessionLocal() as db:
        # Load workflow run and the associated project
        db_workflow = await db.get(WorkflowRun, workflow_id)
        if not db_workflow:
            logger.error("Workflow run not found", workflow_id=workflow_id)
            return

        db_project = await db.get(Project, db_workflow.project_id)
        if not db_project:
            logger.error("Project not found for workflow", project_id=db_workflow.project_id)
            db_workflow.status = WorkflowStatus.FAILED
            db_workflow.logs = "Associated project was not found."
            db.add(db_workflow)
            await db.commit()
            return

        project_title = db_project.title
        target_audience = db_project.settings.get("target_audience", "General Learners")
        objectives = db_project.settings.get("objectives", ["Learn the fundamentals"])
        additional_context = db_project.settings.get("additional_context", "")

    try:
        # 1. Needs Analysis Phase
        logger.info("Executing Analysis phase", workflow_id=workflow_id)
        analysis_data = await ai_service.generate_needs_analysis(
            project_id=db_project.id,
            title=project_title,
            target_audience=target_audience,
            objectives=objectives,
            additional_context=additional_context,
        )

        async with AsyncSessionLocal() as db:
            db_workflow = await db.get(WorkflowRun, workflow_id)
            db_workflow.current_phase = WorkflowPhase.DESIGN
            db_workflow.state_data = {"analysis": analysis_data}
            db_workflow.logs = (db_workflow.logs or "") + "\n[System] Completed Phase: ANALYSIS"
            db.add(db_workflow)
            await db.commit()

        # 2. Design Phase
        logger.info("Executing Design phase", workflow_id=workflow_id)
        design_data = await ai_service.generate_curriculum_outline(
            project_id=db_project.id,
            analysis_results=analysis_data,
        )

        async with AsyncSessionLocal() as db:
            db_workflow = await db.get(WorkflowRun, workflow_id)
            db_workflow.current_phase = WorkflowPhase.DEVELOP
            db_workflow.state_data = {"design": design_data}
            db_workflow.logs = (db_workflow.logs or "") + "\n[System] Completed Phase: DESIGN"
            db.add(db_workflow)
            await db.commit()

        # 3. Development Phase
        logger.info("Executing Development phase", workflow_id=workflow_id)
        develop_data = await ai_service.generate_storyboard(
            project_id=db_project.id,
            design_results=design_data,
        )

        async with AsyncSessionLocal() as db:
            db_workflow = await db.get(WorkflowRun, workflow_id)
            db_workflow.current_phase = WorkflowPhase.REVIEW
            db_workflow.state_data = {"development": develop_data}
            db_workflow.logs = (db_workflow.logs or "") + "\n[System] Completed Phase: DEVELOP"
            db.add(db_workflow)
            await db.commit()

        # 4. Review Phase
        logger.info("Executing Review phase", workflow_id=workflow_id)
        review_data = await ai_service.review_content(
            project_id=db_project.id,
            developed_content=develop_data,
        )

        async with AsyncSessionLocal() as db:
            db_workflow = await db.get(WorkflowRun, workflow_id)
            db_workflow.status = WorkflowStatus.COMPLETED
            db_workflow.state_data = {"review": review_data}
            db_workflow.logs = (db_workflow.logs or "") + "\n[System] Completed Phase: REVIEW\n[System] Workflow Run Succeeded!"
            db.add(db_workflow)
            await db.commit()

        logger.info("Workflow run completed successfully", workflow_id=workflow_id)

    except Exception as e:
        logger.error("Error executing background workflow pipeline", workflow_id=workflow_id, error=str(e))
        async with AsyncSessionLocal() as db:
            db_workflow = await db.get(WorkflowRun, workflow_id)
            if db_workflow:
                db_workflow.status = WorkflowStatus.FAILED
                db_workflow.logs = (db_workflow.logs or "") + f"\n[System Error] Execution aborted: {str(e)}"
                db.add(db_workflow)
                await db.commit()


@celery_app.task(name="app.tasks.ai_generation_task.run_workflow_pipeline_task")
def run_workflow_pipeline_task(workflow_id: str, organization_id: str) -> None:
    """Celery background task to trigger the complete agentic L&D design process."""
    asyncio.run(_async_run_workflow(workflow_id, organization_id))
