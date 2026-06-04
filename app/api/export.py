from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_organization_id, get_current_user
from app.db.session import get_db
from app.models.user import User
from app.services.export_service import ExportService
from app.services.project_service import ProjectService

router = APIRouter()


@router.get("/pdf/{project_id}")
async def export_pdf(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    organization_id: int = Depends(get_current_organization_id),
    current_user: User = Depends(get_current_user),
):
    project = await ProjectService.get_project(db, project_id, organization_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

    file_path = await ExportService.export_pdf(db, project_id, organization_id)
    if not file_path or not Path(file_path).exists():
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate PDF export.")

    return FileResponse(path=file_path, media_type="application/pdf", filename=Path(file_path).name)


@router.get("/docx/{project_id}")
async def export_docx(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    organization_id: int = Depends(get_current_organization_id),
    current_user: User = Depends(get_current_user),
):
    project = await ProjectService.get_project(db, project_id, organization_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

    file_path = await ExportService.export_docx(db, project_id, organization_id)
    if not file_path or not Path(file_path).exists():
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate DOCX export.")

    return FileResponse(path=file_path, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename=Path(file_path).name)


@router.get("/ppt/{project_id}")
async def export_ppt(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    organization_id: int = Depends(get_current_organization_id),
    current_user: User = Depends(get_current_user),
):
    project = await ProjectService.get_project(db, project_id, organization_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

    file_path = await ExportService.export_ppt(db, project_id, organization_id)
    if not file_path or not Path(file_path).exists():
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate PPT export.")

    return FileResponse(path=file_path, media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation", filename=Path(file_path).name)
