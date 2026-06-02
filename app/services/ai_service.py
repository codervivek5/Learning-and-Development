from typing import Any, Dict, List, Optional
from app.agents.analysis_agent import AnalysisAgent
from app.agents.curriculum_agent import CurriculumAgent
from app.agents.storyboard_agent import StoryboardAgent
from app.agents.review_agent import ReviewAgent
from app.schemas.ai import AICurriculumRequest, AICurriculumResponse
from app.providers import get_provider


class AIService:
    """Service to coordinate AI generation and multi-agent workflows."""

    def __init__(self) -> None:
        self.analysis_agent = AnalysisAgent()
        self.curriculum_agent = CurriculumAgent()
        self.storyboard_agent = StoryboardAgent()
        self.review_agent = ReviewAgent()

    async def generate_needs_analysis(
        self,
        project_id: int,
        title: str,
        target_audience: str,
        objectives: List[str],
        additional_context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Perform Needs Analysis by triggering the AnalysisAgent."""
        return await self.analysis_agent.run(
            project_id=project_id,
            title=title,
            target_audience=target_audience,
            objectives=objectives,
            additional_context=additional_context,
        )

    async def generate_curriculum_outline(
        self,
        project_id: int,
        analysis_results: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate the curriculum outline based on Needs Analysis."""
        return await self.curriculum_agent.run(
            project_id=project_id,
            analysis_results=analysis_results,
        )

    async def generate_storyboard(
        self,
        project_id: int,
        design_results: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate detailed storyboard and slide scripts based on design outline."""
        return await self.storyboard_agent.run(
            project_id=project_id,
            design_results=design_results,
        )

    async def review_content(
        self,
        project_id: int,
        developed_content: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Run SME/QC review and generate a structural audit report."""
        return await self.review_agent.run(
            project_id=project_id,
            developed_content=developed_content,
        )

    async def generate_structured_curriculum(
        self,
        request: AICurriculumRequest,
    ) -> AICurriculumResponse:
        """Helper method to generate direct structured curriculum validated by Pydantic."""
        provider = get_provider()
        prompt = f"""
        Design a structured curriculum for:
        Course Title: {request.title}
        Target Audience: {request.target_audience}
        Learning Objectives: {request.objectives}
        Additional Info: {request.additional_context or 'None'}
        """
        system_instruction = "You are a professional educational developer."
        
        # Requests structured validated class output
        return await provider.generate_structured(
            prompt=prompt,
            response_schema=AICurriculumResponse,
            system_instruction=system_instruction,
        )
