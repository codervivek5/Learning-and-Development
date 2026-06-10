from typing import Dict, Any

from app.providers import get_provider
from app.schemas.review import ReviewResponse
from app.core.logging import get_logger

logger = get_logger(__name__)


async def evaluate_review_node(state: Dict[str, Any]) -> Dict[str, Any]:
    provider = get_provider()
    content = state["developed_content"]

    prompt = f"""
You are a senior quality reviewer for corporate L&D content.
Audit the course material below for clarity, alignment to objectives, and improvement recommendations.

Developed content:
{content}

Return only valid JSON matching the schema:
{{
  "score": 0,
  "strengths": ["..."],
  "improvements": ["..."],
  "approved": true
}}
"""

    system_instruction = "You are a professional L&D quality assessor."

    logger.info("Running review evaluation")
    try:
        response = await provider.generate_structured(
            prompt=prompt,
            response_schema=ReviewResponse,
            system_instruction=system_instruction,
        )
        return {"review_output": response.model_dump()}
    except Exception as e:
        logger.error("Review LLM execution failed", error=str(e))
        return {"error": str(e), "review_output": {}}
