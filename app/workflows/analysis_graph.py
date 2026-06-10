from typing import Dict, Any, List, Optional
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END

from app.providers import get_provider
from app.vectorstore.retriever import retrieve_context
from app.schemas.analysis import AnalysisOutput
from app.core.logging import get_logger

logger = get_logger(__name__)


class AnalysisState(TypedDict):
    project_id: int
    title: str
    target_audience: str
    objectives: List[str]
    additional_context: Optional[str]
    retrieved_context: List[str]
    analysis_output: Dict[str, Any]
    error: Optional[str]


async def retrieve_context_node(state: AnalysisState) -> Dict[str, Any]:
    project_id = state["project_id"]
    query = (
        f"Target Audience: {state['target_audience']}. "
        f"Objectives: {', '.join(state['objectives'])}."
    )
    logger.info("Retrieving context in analysis graph", project_id=project_id, query=query)

    chunks = await retrieve_context(project_id, query, limit=3)
    retrieved_texts = [chunk["content"] for chunk in chunks]

    return {"retrieved_context": retrieved_texts}


async def generate_analysis_node(state: AnalysisState) -> Dict[str, Any]:
    provider = get_provider()

    context_str = "\n---\n".join(state.get("retrieved_context", []))
    prompt = f"""
You are an expert Instructional Designer. Perform a comprehensive Needs Assessment and Learner Analysis for the following learning project:

Course Title: {state['title']}
Target Audience: {state['target_audience']}
Core Objectives: {', '.join(state['objectives'])}
Additional Context: {state.get('additional_context') or 'None'}

Reference Materials:
{context_str or 'No reference documents provided.'}

Return only valid JSON matching the schema below:
{{
  "learner_profile": "...",
  "knowledge_gaps": ["..."],
  "delivery_recommendations": "...",
  "assessment_strategy": "...",
  "constraints_and_risks": "..."
}}
"""

    system_instruction = "You are a professional instructional design consultant."

    logger.info("Generating needs assessment using LLM provider")
    try:
        response = await provider.generate_structured(
            prompt=prompt,
            response_schema=AnalysisOutput,
            system_instruction=system_instruction,
        )

        return {"analysis_output": response.model_dump()}
    except Exception as e:
        logger.error("Analysis LLM execution failed", error=str(e))
        return {"error": str(e), "analysis_output": {}}


workflow = StateGraph(AnalysisState)
workflow.add_node("retrieve_context", retrieve_context_node)
workflow.add_node("generate_analysis", generate_analysis_node)
workflow.set_entry_point("retrieve_context")
workflow.add_edge("retrieve_context", "generate_analysis")
workflow.add_edge("generate_analysis", END)
analysis_graph = workflow.compile()
