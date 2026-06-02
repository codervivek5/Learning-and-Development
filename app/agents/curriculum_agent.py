import uuid
from typing import Dict, Any, List, Optional
from app.workflows.design_graph import design_graph
from app.core.logging import get_logger

logger = get_logger(__name__)


class CurriculumAgent:
    """Agent that coordinates the Curriculum outline and design phase."""

    async def run(
        self,
        project_id: uuid.UUID,
        analysis_results: Dict[str, Any],
    ) -> Dict[str, Any]:
        logger.info("Running Curriculum Agent", project_id=project_id)

        # Initial state setup
        initial_state = {
            "project_id": project_id,
            "analysis_results": analysis_results,
            "design_output": {},
            "error": None,
        }

        # Execute Graph
        final_state = await design_graph.ainvoke(initial_state)

        if final_state.get("error"):
            logger.error("Curriculum Agent execution completed with error", project_id=project_id, error=final_state["error"])
            return {"status": "error", "error": final_state["error"]}

        logger.info("Curriculum Agent execution completed successfully", project_id=project_id)
        return final_state.get("design_output", {})
