from typing import Dict, Any
from app.workflows.review_graph import review_graph
from app.schemas.review import ReviewResponse
from app.core.logging import get_logger

logger = get_logger(__name__)


class ReviewAgent:
    """Agent that coordinates e-learning review and auditing phase."""

    async def run(
        self,
        project_id: int,
        developed_content: Dict[str, Any],
    ) -> ReviewResponse:
        logger.info("Running Review Agent", project_id=project_id)

        initial_state = {
            "project_id": project_id,
            "developed_content": developed_content,
            "review_output": {},
            "error": None,
        }

        final_state = await review_graph.ainvoke(initial_state)

        if error := final_state.get("error"):
            logger.error(
                "Review Agent completed with error",
                project_id=project_id,
                error=error,
            )
            raise RuntimeError(error)

        review_output = final_state.get("review_output", {})
        return ReviewResponse.model_validate(review_output)
