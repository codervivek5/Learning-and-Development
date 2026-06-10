# app/agents/analysis_agent.py
from typing import List, Optional
from app.workflows.analysis_graph import analysis_graph
from app.schemas.analysis import AnalysisOutput, AnalysisResponse
from app.core.logging import get_logger

logger = get_logger(__name__)


class AnalysisAgent:
    """Agent that coordinates the Needs Assessment & Gap Analysis phase."""

    async def run(
        self,
        project_id: int,
        title: str,
        target_audience: str,
        objectives: List[str],
        additional_context: Optional[str] = None,
    ) -> AnalysisResponse:
        logger.info("Running Analysis Agent", project_id=project_id)

        initial_state = {
            "project_id": project_id,
            "title": title,
            "target_audience": target_audience,
            "objectives": objectives,
            "additional_context": additional_context,
            "retrieved_context": [],
            "analysis_output": {},
            "error": None,
        }

        final_state = await analysis_graph.ainvoke(initial_state)

        if error := final_state.get("error"):
            logger.error(
                "Analysis Agent execution completed with error",
                project_id=project_id,
                error=error,
            )
            raise RuntimeError(error)

        analysis_output = final_state.get("analysis_output", {})
        return AnalysisResponse(phase="analysis", output=AnalysisOutput.model_validate(analysis_output))

