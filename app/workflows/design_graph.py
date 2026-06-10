from typing import Dict, Any, Optional
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END

from app.nodes.design_nodes import generate_design_structure_node
from app.core.logging import get_logger

logger = get_logger(__name__)


class DesignState(TypedDict):
    project_id: int
    analysis_results: Dict[str, Any]
    design_output: Dict[str, Any]
    error: Optional[str]


workflow = StateGraph(DesignState)
workflow.add_node("generate_design", generate_design_structure_node)
workflow.set_entry_point("generate_design")
workflow.add_edge("generate_design", END)

design_graph = workflow.compile()
