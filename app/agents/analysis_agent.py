import uuid
from typing import Dict, Any, List, Optional
from app.workflows.analysis_graph import analysis_graph
from app.core.logging import get_logger

logger = get_logger(__name__)


class AnalysisAgent:
    """Agent that coordinates the Needs Assessment & Gap Analysis phase."""

    async def run(
        self,
        project_id: uuid.UUID,
        title: str,
        target_audience: str,
        objectives: List[str],
        additional_context: Optional[str] = None,
    ) -> Dict[str, Any]:
        logger.info("Running Analysis Agent", project_id=project_id)

        # Initial state setup
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

        # Execute Graph
        final_state = await analysis_graph.ainvoke(initial_state)

        if final_state.get("error"):
            logger.error("Analysis Agent execution completed with error", project_id=project_id, error=final_state["error"])
            return {"status": "error", "error": final_state["error"]}

        logger.info("Analysis Agent execution completed successfully", project_id=project_id)
        return final_state.get("analysis_output", {})

