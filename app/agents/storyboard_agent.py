import uuid
from typing import Dict, Any, List, Optional
from app.workflows.develop_graph import develop_graph
from app.core.logging import get_logger

logger = get_logger(__name__)


class StoryboardAgent:
    """Agent that coordinates the content writing and storyboarding phase."""

    async def run(
        self,
        project_id: uuid.UUID,
        design_results: Dict[str, Any],
    ) -> Dict[str, Any]:
        logger.info("Running Storyboard Agent", project_id=project_id)

        # Initial state setup
        initial_state = {
            "project_id": project_id,
            "design_results": design_results,
            "development_output": {},
            "error": None,
        }

        # Execute Graph
        final_state = await develop_graph.ainvoke(initial_state)

        if final_state.get("error"):
            logger.error("Storyboard Agent execution completed with error", project_id=project_id, error=final_state["error"])
            return {"status": "error", "error": final_state["error"]}

        logger.info("Storyboard Agent execution completed successfully", project_id=project_id)
        return final_state.get("development_output", {})
