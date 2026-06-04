import asyncio
from app.tasks.celery_app import celery_app
from app.core.database import AsyncSessionLocal
from app.models.workflow import WorkflowRun
from app.models.project import Project
from app.core.constants import WorkflowPhase, WorkflowStatus
from app.schemas.analysis import AnalysisRequest
from app.services.ai_service import AIService
from app.services.training_content_service import TrainingContentService
from app.core.logging import get_logger

logger = get_logger(__name__)


async def _async_run_workflow(workflow_id_str: str, organization_id_str: str) -> None:
    workflow_id = int(workflow_id_str)
    organization_id = int(organization_id_str)

    ai_service = AIService()

    async with AsyncSessionLocal() as db:
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

    try:
        analysis_request = AnalysisRequest(
            title=db_project.title,
            target_audience=db_project.settings.get("target_audience", "General Learners"),
            objectives=db_project.settings.get("objectives", []),
            additional_context=db_project.settings.get("additional_context", ""),
        )

        logger.info("Executing Analysis phase", workflow_id=workflow_id)
        analysis_output = await ai_service.generate_needs_analysis(
            project_id=db_project.id,
            request=analysis_request,
        )

        async with AsyncSessionLocal() as db:
            db_workflow = await db.get(WorkflowRun, workflow_id)
            db_workflow.current_phase = WorkflowPhase.DESIGN
            db_workflow.state_data = {"analysis": analysis_output.model_dump()}
            db_workflow.logs = (db_workflow.logs or "") + "\n[System] Completed Phase: ANALYSIS"
            db.add(db_workflow)
            await db.commit()
            await TrainingContentService.save_phase_output(
                db=db,
                project_id=db_project.id,
                phase="analysis",
                content=analysis_output.model_dump(),
                organization_id=organization_id,
            )

        design_output = await ai_service.generate_design(
            project_id=db_project.id,
            analysis_results=analysis_output.output.model_dump(),
        )

        async with AsyncSessionLocal() as db:
            db_workflow = await db.get(WorkflowRun, workflow_id)
            db_workflow.current_phase = WorkflowPhase.DEVELOP
            db_workflow.state_data = {"design": design_output.model_dump()}
            db_workflow.logs = (db_workflow.logs or "") + "\n[System] Completed Phase: DESIGN"
            db.add(db_workflow)
            await db.commit()
            await TrainingContentService.save_phase_output(
                db=db,
                project_id=db_project.id,
                phase="design",
                content=design_output.model_dump(),
                organization_id=organization_id,
            )

        develop_output = await ai_service.generate_development(
            project_id=db_project.id,
            design_results=design_output.model_dump(),
        )

        async with AsyncSessionLocal() as db:
            db_workflow = await db.get(WorkflowRun, workflow_id)
            db_workflow.current_phase = WorkflowPhase.REVIEW
            db_workflow.state_data = {"develop": develop_output.model_dump()}
            db_workflow.logs = (db_workflow.logs or "") + "\n[System] Completed Phase: DEVELOP"
            db.add(db_workflow)
            await db.commit()
            await TrainingContentService.save_phase_output(
                db=db,
                project_id=db_project.id,
                phase="develop",
                content=develop_output.model_dump(),
                organization_id=organization_id,
            )

        review_output = await ai_service.generate_review(
            project_id=db_project.id,
            developed_content=develop_output.model_dump(),
        )

        async with AsyncSessionLocal() as db:
            db_workflow = await db.get(WorkflowRun, workflow_id)
            db_workflow.status = WorkflowStatus.COMPLETED
            db_workflow.state_data = {"review": review_output.model_dump()}
            db_workflow.logs = (db_workflow.logs or "") + "\n[System] Completed Phase: REVIEW\n[System] Workflow Run Succeeded!"
            db.add(db_workflow)
            await db.commit()
            await TrainingContentService.save_phase_output(
                db=db,
                project_id=db_project.id,
                phase="review",
                content=review_output.model_dump(),
                organization_id=organization_id,
            )

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
