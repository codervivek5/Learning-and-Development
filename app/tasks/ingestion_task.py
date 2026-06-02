import asyncio
import uuid
from app.tasks.celery_app import celery_app
from app.vectorstore.ingestion import ingest_document
from app.core.database import AsyncSessionLocal
from app.models.document import Document
from app.core.logging import get_logger

logger = get_logger(__name__)


async def _async_ingest_document(project_id_str: str, document_id_str: str, file_path: str) -> None:
    project_id = uuid.UUID(project_id_str)
    document_id = uuid.UUID(document_id_str)

    logger.info("Executing async ingestion workflow", document_id=document_id)
    success = await ingest_document(project_id, file_path, document_id)

    if success:
        # Update database status
        async with AsyncSessionLocal() as db:
            db_document = await db.get(Document, document_id)
            if db_document:
                db_document.is_embedded = True
                db.add(db_document)
                await db.commit()
                logger.info("Updated document database status to embedded", document_id=document_id)
    else:
        logger.error("Failed to ingest document", document_id=document_id)


@celery_app.task(name="app.tasks.ingestion_task.ingest_document_task")
def ingest_document_task(project_id_str: str, document_id_str: str, file_path: str) -> None:
    """Celery background task wrapper for document ingestion."""
    asyncio.run(_async_ingest_document(project_id_str, document_id_str, file_path))
