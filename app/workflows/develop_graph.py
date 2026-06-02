import uuid
from typing import Dict, Any, List, Optional
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END

from app.providers import get_provider
from app.core.logging import get_logger

logger = get_logger(__name__)


class DevelopState(TypedDict):
    project_id: uuid.UUID
    design_results: Dict[str, Any]
    development_output: Dict[str, Any]
    error: Optional[str]


async def generate_module_content_node(state: DevelopState) -> Dict[str, Any]:
    """Generate detailed slide content, narration scripts, and exercises."""
    provider = get_provider()
    curriculum_outline = state["design_results"].get("curriculum_outline", "")

    prompt = f"""
    You are an expert Content Developer and Copywriter for L&D training.
    Develop the full training script and content based on this outline:

    Curriculum Outline:
    {curriculum_outline}

    Generate the complete module scripts, including:
    - Detailed slide-by-slide copy
    - Narration/speaker notes for the trainer or voiceover
    - Interactive check-for-understanding questions and quizzes
    - Practical exercises
    """

    system_instruction = "You are a professional training content writer."

    logger.info("Generating module scripts in develop graph")
    try:
        response_text = await provider.generate_text(
            prompt=prompt,
            system_instruction=system_instruction,
        )
        return {
            "development_output": {
                "course_content": response_text,
                "status": "success",
            }
        }
    except Exception as e:
        logger.error("Development LLM execution failed", error=str(e))
        return {"error": str(e), "development_output": {"status": "failed"}}


# Define the Graph
workflow = StateGraph(DevelopState)

# Add Nodes
workflow.add_node("generate_content", generate_module_content_node)

# Set Entry and Edges
workflow.set_entry_point("generate_content")
workflow.add_edge("generate_content", END)

# Compile
develop_graph = workflow.compile()
