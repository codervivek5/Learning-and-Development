from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.deps import get_current_user, get_current_organization_id
from app.models.user import User
from app.services.upload_service import UploadService
from app.models.document import Document

router = APIRouter()


@router.post("/{project_id}", response_model=dict, status_code=status.HTTP_201_CREATED)
async def upload_document(
    project_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    organization_id: int = Depends(get_current_organization_id),
    current_user: User = Depends(get_current_user),
):
    """Upload a training material document (PDF/Word/PPT) for AI context."""
    # Check mime type support
    allowed_mimes = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "text/plain",
    ]
    if file.content_type not in allowed_mimes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file format. Please upload PDF, DOCX, PPTX or TXT."
        )

    db_doc = await UploadService.upload_document(
        db=db,
        file=file,
        project_id=project_id,
        organization_id=organization_id,
    )
    return {
        "message": "File uploaded successfully, parsing started in background.",
        "document_id": db_doc.id,
        "filename": db_doc.filename,
    }


@router.get("/{project_id}", response_model=List[dict])
async def list_project_documents(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    organization_id: int = Depends(get_current_organization_id),
    current_user: User = Depends(get_current_user),
):
    """Retrieve metadata of all uploaded documents for a project."""
    docs = await UploadService.get_project_documents(
        db=db, project_id=project_id, organization_id=organization_id
    )
    return [
        {
            "id": doc.id,
            "filename": doc.filename,
            "file_size": f"{round(doc.file_size / 1024, 2) if doc.file_size else 0} KB",
            "is_embedded": doc.is_embedded,
            "created_at": doc.created_at,
        }
        for doc in docs
    ]
