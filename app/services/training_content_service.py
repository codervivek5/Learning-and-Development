from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.training_content import TrainingContent


class TrainingContentService:
    """CRUD for phase-by-phase training content produced by ADDIE workflows."""

    @staticmethod
    async def save_phase_output(
        db: AsyncSession,
        project_id: int,
        phase: str,
        content: dict,
    ) -> TrainingContent:
        training_content = TrainingContent(
            project_id=project_id,
            phase=phase,
            content=content,
        )
        db.add(training_content)
        await db.commit()
        await db.refresh(training_content)
        return training_content

    @staticmethod
    async def get_latest_phase_output(
        db: AsyncSession,
        project_id: int,
        phase: str,
    ) -> Optional[TrainingContent]:
        result = await db.execute(
            select(TrainingContent)
            .where(
                TrainingContent.project_id == project_id,
                TrainingContent.phase == phase,
            )
            .order_by(TrainingContent.id.desc())
            .limit(1)
        )
        return result.scalars().first()
