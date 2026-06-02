import asyncio
from app.tasks.celery_app import celery_app
from app.core.logging import get_logger

logger = get_logger(__name__)


async def _async_compute_batch_embeddings() -> None:
    logger.info("Batch embedding calculation task started (mocked)")
    await asyncio.sleep(1)
    logger.info("Batch embedding calculation completed successfully")


@celery_app.task(name="app.tasks.embeddings_task.compute_batch_embeddings_task")
def compute_batch_embeddings_task() -> None:
    """Mock Celery task for future bulk embeddings calculation."""
    asyncio.run(_async_compute_batch_embeddings())
