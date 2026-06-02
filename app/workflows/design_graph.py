import uuid
from typing import Dict, Any, List, Optional
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END

from app.providers import get_provider
from app.core.logging import get_logger

logger = get_logger(__name__)


class DesignState(TypedDict):
    project_id: uuid.UUID
    analysis_results: Dict[str, Any]
    design_output: Dict[str, Any]
    error: Optional[str]


async def generate_curriculum_structure_node(state: DesignState) -> Dict[str, Any]:
    """Generate the curriculum structure and module maps based on the analysis output."""
    provider = get_provider()
    analysis_text = state["analysis_results"].get("needs_assessment", "")

    prompt = f"""
    You are an expert Instructional Designer. Using the Needs Assessment and Learner Analysis below, design the curriculum structure/outline.

    Needs Assessment Context:
    {analysis_text}

    Provide a structured curriculum plan including:
    1. Overall Course Structure (Modules 1 to N)
    2. Estimated Duration for each Module
    3. Learning Objectives mapped to each Module
    4. Assessment strategies for verifying objective completion
    """

    system_instruction = "You are a professional instructional design consultant specializing in curriculum mapping."

    logger.info("Generating curriculum outline in design graph")
    try:
        response_text = await provider.generate_text(
            prompt=prompt,
            system_instruction=system_instruction,
        )
        return {
            "design_output": {
                "curriculum_outline": response_text,
                "status": "success",
            }
        }
    except Exception as e:
        logger.error("Design LLM execution failed", error=str(e))
        return {"error": str(e), "design_output": {"status": "failed"}}


# Define the Graph
workflow = StateGraph(DesignState)

# Add Nodes
workflow.add_node("generate_curriculum", generate_curriculum_structure_node)

# Set Entry and Edges
workflow.set_entry_point("generate_curriculum")
workflow.add_edge("generate_curriculum", END)

# Compile
design_graph = workflow.compile()
