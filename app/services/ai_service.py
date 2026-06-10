import json
import re
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.analysis_agent import AnalysisAgent
from app.agents.curriculum_agent import CurriculumAgent
from app.agents.development_agent import DevelopmentAgent
from app.agents.review_agent import ReviewAgent
from app.providers import get_provider
from app.prompts import (
    INTERACTIVITY_SYSTEM_INSTRUCTION,
    OBJECTIVES_SYSTEM_INSTRUCTION,
)
from app.schemas.ai import AIInteractivityResponse, AIObjectivesResponse
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
from app.schemas.design import DesignResponse
from app.schemas.development import DevelopmentResponse
from app.schemas.review import ReviewResponse
from app.core.logging import get_logger

logger = get_logger(__name__)


class AIService:
    """Service to coordinate AI generation and multi-agent workflows."""

    def __init__(self) -> None:
        self.analysis_agent = AnalysisAgent()
        self.curriculum_agent = CurriculumAgent()
        self.development_agent = DevelopmentAgent()
        self.review_agent = ReviewAgent()

    async def generate_needs_analysis(
        self,
        project_id: int,
        request: AnalysisRequest,
        db: Optional[AsyncSession] = None,
        user_id: Optional[int] = None,
    ) -> AnalysisResponse:
        """Perform Needs Analysis by triggering the AnalysisAgent."""
        logger.info("Running needs analysis", project_id=project_id, user_id=user_id)
        return await self.analysis_agent.run(
            project_id=project_id,
            title=request.title,
            target_audience=request.target_audience,
            objectives=request.objectives,
            additional_context=request.additional_context,
        )

    async def generate_design(
        self,
        project_id: int,
        analysis_results: dict,
    ) -> DesignResponse:
        """Generate a curriculum design outline using the CurriculumAgent."""
        logger.info("Running design phase", project_id=project_id)
        return await self.curriculum_agent.run(
            project_id=project_id,
            analysis_results=analysis_results,
        )

    async def generate_development(
        self,
        project_id: int,
        design_results: dict,
    ) -> DevelopmentResponse:
        """Generate detailed course content using the DevelopmentAgent."""
        logger.info("Running development phase", project_id=project_id)
        return await self.development_agent.run(
            project_id=project_id,
            design_results=design_results,
        )

    async def generate_review(
        self,
        project_id: int,
        developed_content: dict,
    ) -> ReviewResponse:
        """Run review and quality assurance of developed course content."""
        logger.info("Running review phase", project_id=project_id)
        return await self.review_agent.run(
            project_id=project_id,
            developed_content=developed_content,
        )

    async def generate_ai_objectives(
        self,
        project_id: int,
        content_source: str,
        content: str,
    ) -> AIObjectivesResponse:
        logger.info(
            "Generating AI learning objectives",
            project_id=project_id,
            content_source=content_source,
        )
        provider = get_provider()
        prompt = (
            "Create 4-6 concise, measurable learning objectives from the source content. "
            "Return valid JSON only in the format: {\"objectives\": [\"...\"]}.\n\n"
            f"Source content:\n{content}"
        )

        try:
            return await provider.generate_structured(
                prompt=prompt,
                response_schema=AIObjectivesResponse,
                system_instruction=OBJECTIVES_SYSTEM_INSTRUCTION,
                temperature=0.2,
            )
        except Exception:
            return AIObjectivesResponse(
                objectives=self._extract_list_items_from_text(
                    await provider.generate_text(
                        prompt=prompt,
                        system_instruction=OBJECTIVES_SYSTEM_INSTRUCTION,
                        temperature=0.5,
                    )
                )
            )

    async def generate_ai_interactivity(
        self,
        project_id: int,
        content_source: str,
        content: str,
    ) -> AIInteractivityResponse:
        logger.info(
            "Generating AI interactivity suggestions",
            project_id=project_id,
            content_source=content_source,
        )
        provider = get_provider()
        prompt = (
            "Suggest 3-5 learner interactivity ideas and engagement activities for the source content. "
            "Return valid JSON only in the format: {\"suggestions\": [\"...\"]}.\n\n"
            f"Source content:\n{content}"
        )

        try:
            return await provider.generate_structured(
                prompt=prompt,
                response_schema=AIInteractivityResponse,
                system_instruction=INTERACTIVITY_SYSTEM_INSTRUCTION,
                temperature=0.2,
            )
        except Exception:
            return AIInteractivityResponse(
                suggestions=self._extract_list_items_from_text(
                    await provider.generate_text(
                        prompt=prompt,
                        system_instruction=INTERACTIVITY_SYSTEM_INSTRUCTION,
                        temperature=0.5,
                    )
                )
            )

    @staticmethod
    def _extract_list_items_from_text(raw_text: str) -> List[str]:
        try:
            data = json.loads(raw_text)
            if isinstance(data, list):
                return [str(item).strip() for item in data if item]
            if isinstance(data, dict):
                values = data.get("objectives") or data.get("suggestions")
                if isinstance(values, list):
                    return [str(item).strip() for item in values if item]
        except Exception:
            pass

        lines = []
        for raw_line in raw_text.splitlines():
            line = re.sub(r"^[\-\*•\d\.\)\s]+", "", raw_line).strip()
            if line:
                lines.append(line)

        return lines

    async def generate_text_prompt(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7,
    ) -> str:
        provider = get_provider()
        return await provider.generate_text(
            prompt=prompt,
            system_instruction=system_instruction,
            temperature=temperature,
        )
