import uuid
from typing import Dict, Any, List, Optional
from app.workflows.review_graph import review_graph
from app.core.logging import get_logger

logger = get_logger(__name__)


class ReviewAgent:
    """Agent that coordinates e-learning review and auditing phase."""

    async def run(
        self,
        project_id: uuid.UUID,
        developed_content: Dict[str, Any],
    ) -> Dict[str, Any]:
        logger.info("Running Review Agent", project_id=project_id)

        # Initial state setup
        initial_state = {
            "project_id": project_id,
            "developed_content": developed_content,
            "review_output": {},
            "error": None,
        }

        # Execute Graph
        final_state = await review_graph.ainvoke(initial_state)

        if final_state.get("error"):
            logger.error("Review Agent completed with error", project_id=project_id, error=final_state["error"])
            return {"status": "error", "error": final_state["error"]}

        logger.info("Review Agent completed successfully", project_id=project_id)
        return final_state.get("review_output", {})
