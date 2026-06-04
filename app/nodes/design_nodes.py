from typing import Dict, Any

from app.providers import get_provider
from app.schemas.design import DesignResponse
from app.core.logging import get_logger

logger = get_logger(__name__)


async def generate_design_structure_node(state: Dict[str, Any]) -> Dict[str, Any]:
    provider = get_provider()
    analysis = state["analysis_results"]

    prompt = f"""
You are an expert instructional designer. Use the analysis report below to build a practical course architecture.

Learner Profile: {analysis.get('learner_profile', '')}
Knowledge Gaps: {', '.join(analysis.get('knowledge_gaps', []))}
Delivery Recommendations: {analysis.get('delivery_recommendations', '')}
Assessment Strategy: {analysis.get('assessment_strategy', '')}
Constraints and Risks: {analysis.get('constraints_and_risks', 'None')}

Return only valid JSON matching the schema below:
{{
  "course_title": "...",
  "modules": [
    {{
      "title": "...",
      "description": "...",
      "submodules": [
        {{"title": "...", "description": "..."}}
      ]
    }}
  ]
}}
"""

    system_instruction = "You are a professional curriculum architect."

    logger.info("Generating curriculum design output")
    try:
        response = await provider.generate_structured(
            prompt=prompt,
            response_schema=DesignResponse,
            system_instruction=system_instruction,
        )
        return {"design_output": response.model_dump()}
    except Exception as e:
        logger.error("Design LLM execution failed", error=str(e))
        return {"error": str(e), "design_output": {}}
