from typing import Dict, Any
from app.workflows.design_graph import design_graph
from app.schemas.design import DesignResponse
from app.core.logging import get_logger

logger = get_logger(__name__)


class CurriculumAgent:
    """Agent that coordinates the Curriculum outline and design phase."""

    async def run(
        self,
        project_id: int,
        analysis_results: Dict[str, Any],
    ) -> DesignResponse:
        logger.info("Running Curriculum Agent", project_id=project_id)

        initial_state = {
            "project_id": project_id,
            "analysis_results": analysis_results,
            "design_output": {},
            "error": None,
        }

        final_state = await design_graph.ainvoke(initial_state)

        if error := final_state.get("error"):
            logger.error(
                "Curriculum Agent execution completed with error",
                project_id=project_id,
                error=error,
            )
            raise RuntimeError(error)

        design_output = final_state.get("design_output", {})
        return DesignResponse.model_validate(design_output)
