import uuid
from typing import Dict, Any, List, Optional
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END

from app.providers import get_provider
from app.core.logging import get_logger

logger = get_logger(__name__)


class ReviewState(TypedDict):
    project_id: uuid.UUID
    developed_content: Dict[str, Any]
    review_output: Dict[str, Any]
    error: Optional[str]


async def evaluate_content_node(state: ReviewState) -> Dict[str, Any]:
    """Evaluate training content against standard L&D rubrics."""
    provider = get_provider()
    content = state["developed_content"].get("course_content", "")

    prompt = f"""
    You are an expert SME (Subject Matter Expert) and Quality Reviewer for L&D training.
    Audit the following course script and identify structural gaps, factual accuracy improvements, and educational efficacy.

    Course Content:
    {content}

    Provide feedback covering:
    1. Readability & Tone matching the target audience
    2. Alignment with objectives
    3. Structural clarity
    4. Actionable recommendations for changes
    """

    system_instruction = "You are a professional quality auditor for corporate e-learning and L&D programs."

    logger.info("Evaluating content in review graph")
    try:
        response_text = await provider.generate_text(
            prompt=prompt,
            system_instruction=system_instruction,
        )
        return {
            "review_output": {
                "evaluation_report": response_text,
                "status": "success",
            }
        }
    except Exception as e:
        logger.error("Review LLM execution failed", error=str(e))
        return {"error": str(e), "review_output": {"status": "failed"}}


# Define the Graph
workflow = StateGraph(ReviewState)

# Add Nodes
workflow.add_node("evaluate_content", evaluate_content_node)

# Set Entry and Edges
workflow.set_entry_point("evaluate_content")
workflow.add_edge("evaluate_content", END)

# Compile
review_graph = workflow.compile()
