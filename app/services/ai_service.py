from typing import Any, Dict, List, Optional, Union
from app.agents.analysis_agent import AnalysisAgent
from app.agents.curriculum_agent import CurriculumAgent
from app.agents.storyboard_agent import StoryboardAgent
from app.agents.review_agent import ReviewAgent
from app.schemas.ai import (
    AICurriculumRequest,
    AICurriculumResponse,
    AIObjectivesRequest,
    AIObjectivesResponse,
    AIInteractivityRequest,
    AIInteractivityResponse,
    AIStoryboardRequest,
    AIStoryboardResponse,
)
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
        request: Union[AICurriculumRequest, int],
        title: Optional[str] = None,
        target_audience: Optional[str] = None,
        objectives: Optional[List[str]] = None,
        additional_context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Perform Needs Analysis by triggering the AnalysisAgent."""
        if isinstance(request, AICurriculumRequest):
            project_id = request.project_id
            title = request.title
            target_audience = request.target_audience
            objectives = request.objectives
            additional_context = request.additional_context
        else:
            project_id = request

        return await self.analysis_agent.run(
            project_id=project_id,
            title=title or "",
            target_audience=target_audience or "",
            objectives=objectives or [],
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

    async def generate_objectives(
        self,
        request: AIObjectivesRequest,
    ) -> AIObjectivesResponse:
        """Generate fine-grained objectives from provided content metadata."""
        provider = get_provider()
        prompt = f"""
        Generate measurable learning objectives for the following course content.
        Project ID: {request.project_id}
        Content Source: {request.content_source}
        Content: {request.content}
        Target Audience: {request.target_audience_description}
        Prior Knowledge Level: {request.prior_knowledge_level or 'Not specified'}
        Job Roles: {', '.join(request.job_roles) if request.job_roles else 'None'}
        Primary Language: {request.primary_language or 'Not specified'}
        Learner Location: {request.learner_location or 'Not specified'}
        Additional Context: {request.additional_context or 'None'}
        """
        system_instruction = "You are an instructional designer that writes concise, measurable learning objectives."

        return await provider.generate_structured(
            prompt=prompt,
            response_schema=AIObjectivesResponse,
            system_instruction=system_instruction,
        )

    async def generate_interactivity_suggestions(
        self,
        request: AIInteractivityRequest,
    ) -> AIInteractivityResponse:
        """Generate interactive learning suggestions from text and source context."""
        provider = get_provider()
        prompt = f"""
        Recommend instructional interactivity suggestions based on the content below.
        Project ID: {request.project_id}
        Content Source: {request.content_source}
        Content: {request.content or 'No content provided'}
        """
        system_instruction = "You are an instructional designer who suggests engaging interactive elements."

        return await provider.generate_structured(
            prompt=prompt,
            response_schema=AIInteractivityResponse,
            system_instruction=system_instruction,
        )

    async def generate_storyboard_slides(
        self,
        request: AIStoryboardRequest,
    ) -> AIStoryboardResponse:
        """Generate storyboard slide specifications from a topic outline and learning goals."""
        provider = get_provider()
        prompt = f"""
        Create a sequence of storyboard slides for the following topic outline.
        Project ID: {request.project_id}
        Topic Outline: {request.topic_outline}
        Learning Goals: {', '.join(request.learning_goals)}
        """
        system_instruction = "You are a storyboard designer. Output a set of slides with titles, narration, duration, transitions, and visual prompts."

        return await provider.generate_structured(
            prompt=prompt,
            response_schema=AIStoryboardResponse,
            system_instruction=system_instruction,
        )
