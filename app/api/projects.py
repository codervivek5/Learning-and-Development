from typing import List, Optional
from fastapi import APIRouter, Depends, Form, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
import json
from app.db.session import get_db
from app.api.deps import get_current_user, get_current_organization_id
from app.models.user import User
from app.services.project_service import ProjectService
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse

router = APIRouter()


@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    organization_id: int = Depends(get_current_organization_id),
    current_user: User = Depends(get_current_user),
):
    """Retrieve all design projects belonging to the active organization tenant."""
    return await ProjectService.get_projects(
        db=db, organization_id=organization_id, skip=skip, limit=limit
    )


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
        title: str = Form(..., description="Project name"),
        description: Optional[str] = Form(None, description="Project description"),
        db: AsyncSession = Depends(get_db),
        organization_id: int = Depends(get_current_organization_id),
        current_user: User = Depends(get_current_user),
):
    """Create a new e-learning design project via Form Data."""
    # Instantiating the expected Pydantic model internally so service logic doesn't break
    project_in = ProjectCreate(title=title, description=description)

    return await ProjectService.create_project(
        db=db, project_in=project_in, organization_id=organization_id
    )


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    organization_id: int = Depends(get_current_organization_id),
    current_user: User = Depends(get_current_user),
):
    """Retrieve details of a specific project."""
    project = await ProjectService.get_project(
        db=db, project_id=project_id, organization_id=organization_id
    )
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    return project


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int = Path(..., description="The ID of the project to update"),
    title: Optional[str] = Form(None, description="Updated project title"),
    description: Optional[str] = Form(None, description="Updated project description"),
    settings: Optional[str] = Form(None, description="Updated project settings as a JSON string"),
    db: AsyncSession = Depends(get_db),
    organization_id: int = Depends(get_current_organization_id),
    current_user: User = Depends(get_current_user),
):
    """Update settings or details of a project partially via PATCH Form Data."""
    parsed_settings = None
    if settings:
        try:
            parsed_settings = json.loads(settings)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON format provided for settings field."
            )

    # Creating ProjectUpdate schema instance with mapped parameters
    project_in = ProjectUpdate(title=title, description=description, settings=parsed_settings)

    project = await ProjectService.update_project(
        db=db,
        project_id=project_id,
        project_in=project_in,
        organization_id=organization_id,
    )
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or unauthorized",
        )
    return project


@router.delete("/{project_id}", status_code=status.HTTP_200_OK)
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    organization_id: int = Depends(get_current_organization_id),
    current_user: User = Depends(get_current_user),
):
    """Delete a design project."""
    success = await ProjectService.delete_project(
        db=db, project_id=project_id, organization_id=organization_id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or unauthorized",
        )
    return {
        "status": "success",
        "message": f"Project with ID {project_id} deleted successfully."
    }
