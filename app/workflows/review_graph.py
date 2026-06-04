from typing import Dict, Any, Optional
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END

from app.nodes.review_nodes import evaluate_review_node
from app.core.logging import get_logger

logger = get_logger(__name__)


class ReviewState(TypedDict):
    project_id: int
    developed_content: Dict[str, Any]
    review_output: Dict[str, Any]
    error: Optional[str]


workflow = StateGraph(ReviewState)
workflow.add_node("evaluate_review", evaluate_review_node)
workflow.set_entry_point("evaluate_review")
workflow.add_edge("evaluate_review", END)

review_graph = workflow.compile()
