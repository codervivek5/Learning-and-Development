from typing import Dict, Any

from app.providers import get_provider
from app.schemas.development import DevelopmentResponse
from app.core.logging import get_logger

logger = get_logger(__name__)


async def generate_development_node(state: Dict[str, Any]) -> Dict[str, Any]:
    provider = get_provider()
    design = state["design_results"]

    prompt = f"""
You are an expert learning experience developer. Convert the curriculum design below into high-quality course content.

Course Title: {design.get('course_title', '')}
Modules: {', '.join([m.get('title', '') for m in design.get('modules', [])])}

Provide JSON only matching the schema:
{{
  "modules": [
    {{
      "title": "...",
      "content": "...",
      "submodules": [
        {{"title": "...", "content": "..."}}
      ]
    }}
  ]
}}
"""

    system_instruction = "You are a professional e-learning content author."

    logger.info("Generating detailed course content")
    try:
        response = await provider.generate_structured(
            prompt=prompt,
            response_schema=DevelopmentResponse,
            system_instruction=system_instruction,
        )
        return {"development_output": response.model_dump()}
    except Exception as e:
        logger.error("Development LLM execution failed", error=str(e))
        return {"error": str(e), "development_output": {}}
