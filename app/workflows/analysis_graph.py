import uuid
from typing import Dict, Any, List, Optional
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END

from app.providers import get_provider
from app.vectorstore.retriever import retrieve_context
from app.core.logging import get_logger

logger = get_logger(__name__)


class AnalysisState(TypedDict):
    project_id: uuid.UUID
    title: str
    target_audience: str
    objectives: List[str]
    additional_context: Optional[str]
    retrieved_context: List[str]
    analysis_output: Dict[str, Any]
    error: Optional[str]


async def retrieve_context_node(state: AnalysisState) -> Dict[str, Any]:
    """Retrieve context from ChromaDB based on the project parameters."""
    project_id = state["project_id"]
    query = f"Target Audience: {state['target_audience']}. Objectives: {', '.join(state['objectives'])}"

    logger.info("Retrieving context in analysis graph", project_id=project_id, query=query)
    chunks = await retrieve_context(project_id, query, limit=3)
    retrieved_texts = [chunk["content"] for chunk in chunks]

    return {"retrieved_context": retrieved_texts}


async def generate_analysis_node(state: AnalysisState) -> Dict[str, Any]:
    """Generate the analysis/needs assessment report using Gemini."""
    provider = get_provider()

    context_str = "\n---\n".join(state.get("retrieved_context", []))
    prompt = f"""
    You are an expert Instructional Designer. Perform a comprehensive Needs Assessment and Learner Analysis for the following course project:

    Course Title: {state['title']}
    Target Audience: {state['target_audience']}
    Core Objectives: {state['objectives']}
    Additional Context: {state.get('additional_context') or "None"}

    Reference Materials Context:
    {context_str or "No reference documents provided."}

    Generate a structured analysis covering:
    1. Learner Profile & Prerequisites
    2. Knowledge/Skill Gap Analysis
    3. Recommended Delivery Methods (e.g. microlearning, scenario-based)
    4. Technical / Learning Constraints
    """

    system_instruction = "You are a professional instructional design consultant."

    logger.info("Generating needs assessment using LLM provider")
    try:
        response_text = await provider.generate_text(
            prompt=prompt,
            system_instruction=system_instruction,
        )
        return {
            "analysis_output": {
                "needs_assessment": response_text,
                "status": "success",
            }
        }
    except Exception as e:
        logger.error("Analysis LLM execution failed", error=str(e))
        return {"error": str(e), "analysis_output": {"status": "failed"}}


# Define the Graph
workflow = StateGraph(AnalysisState)

# Add Nodes
workflow.add_node("retrieve_context", retrieve_context_node)
workflow.add_node("generate_analysis", generate_analysis_node)

# Set Entry and Edges
workflow.set_entry_point("retrieve_context")
workflow.add_edge("retrieve_context", "generate_analysis")
workflow.add_edge("generate_analysis", END)

# Compile Graph
analysis_graph = workflow.compile()
