# app/services/upload_service.py
import asyncio
import os
import shutil
from typing import Sequence
from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import Document
from app.core.logging import get_logger

logger = get_logger(__name__)


class UploadService:
    """Service to handle document uploads and trigger ingestion tasks."""

    @staticmethod
    async def upload_document(
        db: AsyncSession,
        file: UploadFile,
        project_id: int,
        organization_id: int,
    ) -> Document:
        # Create storage uploads folder if not exists
        upload_dir = "./storage/uploads"
        os.makedirs(upload_dir, exist_ok=True)

        _, ext = os.path.splitext(file.filename or "")
        # Use a simple counter-based name; the DB auto-increment id is assigned after commit.
        import uuid as _uuid
        stored_filename = f"{_uuid.uuid4().hex}{ext}"
        file_path = os.path.join(upload_dir, stored_filename)

        logger.info("Saving uploaded file", filename=file.filename, destination=file_path)

        # Save file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Calculate file size
        file_size = os.path.getsize(file_path)

        # Save metadata to database
        db_document = Document(
            project_id=project_id,
            organization_id=organization_id,
            filename=file.filename or "unknown",
            file_path=file_path,
            file_size=file_size,
            mime_type=file.content_type or "application/octet-stream",
            is_embedded=False,
        )

        db.add(db_document)
        await db.commit()
        await db.refresh(db_document)

        logger.info("Document metadata saved", document_id=db_document.id)

        # Trigger background task to parse and embed
        try:
            from app.tasks.ingestion_task import _async_ingest_document
            asyncio.create_task(_async_ingest_document(
                project_id_str=str(project_id),
                document_id_str=str(db_document.id),
                file_path=file_path,
            ))
            logger.info("Started document ingestion in background", document_id=db_document.id)
        except Exception as e:
            logger.error("Failed to start ingestion task", document_id=db_document.id, error=str(e))

        return db_document

    @staticmethod
    async def get_project_documents(
        db: AsyncSession, project_id: int, organization_id: int
    ) -> Sequence[Document]:
        result = await db.execute(
            select(Document).where(
                Document.project_id == project_id,
                Document.organization_id == organization_id,
            )
        )
        return result.scalars().all()
