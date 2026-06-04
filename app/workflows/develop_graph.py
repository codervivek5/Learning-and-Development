from typing import Dict, Any, Optional
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END

from app.nodes.development_nodes import generate_development_node
from app.core.logging import get_logger

logger = get_logger(__name__)


class DevelopState(TypedDict):
    project_id: int
    design_results: Dict[str, Any]
    development_output: Dict[str, Any]
    error: Optional[str]


workflow = StateGraph(DevelopState)
workflow.add_node("generate_development", generate_development_node)
workflow.set_entry_point("generate_development")
workflow.add_edge("generate_development", END)

develop_graph = workflow.compile()
