import asyncio
from app.tasks.celery_app import celery_app
from app.core.logging import get_logger

logger = get_logger(__name__)


async def _async_export_materials(project_id_str: str, format_type: str) -> None:
    logger.info("Material export job started", project_id=project_id_str, format=format_type)
    await asyncio.sleep(2)
    logger.info("Material export completed successfully")


@celery_app.task(name="app.tasks.export_task.export_course_materials_task")
def export_course_materials_task(project_id_str: str, format_type: str) -> None:
    """Mock Celery task to export curriculum/storyboard into PDF/Word/SCORM format."""
    asyncio.run(_async_export_materials(project_id_str, format_type))
