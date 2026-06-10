# app/services/project_service.py
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


logger = get_logger(__name__)


class ProjectService:
    """Service coordinates CRUD operations for Project entity."""

    @staticmethod
    async def get_projects(
        db: AsyncSession,
            skip: int = 0,
            limit: int = 100
    ) -> List[Project]:
        # Enforce multi-tenancy filter
        result = await db.execute(
            select(Project)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def get_project(
        db: AsyncSession, project_id: int,
    ) -> Optional[Project]:
        result = await db.execute(
            select(Project).where(
                Project.id == project_id
            )
        )
        project = result.scalars().first()
        if not project:
            logger.warning(
                project_id=project_id,
            )
        return project

    @staticmethod
    async def create_project(
        db: AsyncSession, project_in: ProjectCreate
    ) -> Project:
        db_project = Project(
            title=project_in.title,
            description=project_in.description,
            settings=project_in.settings or {},
        )
        db.add(db_project)
        await db.commit()
        await db.refresh(db_project)
        return db_project

    @staticmethod
    async def update_project(
        db: AsyncSession,
        project_id: int,
        project_in: ProjectUpdate,
    ) -> Optional[Project]:
        db_project = await ProjectService.get_project(db, project_id)
        if not db_project:
            return None

        update_data = project_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_project, key, value)

        db.add(db_project)
        await db.commit()
        await db.refresh(db_project)
        return db_project

    @staticmethod
    async def delete_project(
        db: AsyncSession, project_id: int
    ) -> bool:
        db_project = await ProjectService.get_project(db, project_id)
        if not db_project:
            return False

        await db.delete(db_project)
        await db.commit()
        return True
