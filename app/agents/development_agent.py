from typing import Dict, Any
from app.workflows.develop_graph import develop_graph
from app.schemas.development import DevelopmentResponse
from app.core.logging import get_logger

logger = get_logger(__name__)


class DevelopmentAgent:
    """Agent that coordinates the content writing and development phase."""

    async def run(
        self,
        project_id: int,
        design_results: Dict[str, Any],
    ) -> DevelopmentResponse:
        logger.info("Running Development Agent", project_id=project_id)

        initial_state = {
            "project_id": project_id,
            "design_results": design_results,
            "development_output": {},
            "error": None,
        }

        final_state = await develop_graph.ainvoke(initial_state)

        if error := final_state.get("error"):
            logger.error(
                "Development Agent execution completed with error",
                project_id=project_id,
                error=error,
            )
            raise RuntimeError(error)

        development_output = final_state.get("development_output", {})
        return DevelopmentResponse.model_validate(development_output)
