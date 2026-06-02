import json
from typing import Any, Dict, List, Optional, Type, Union
from pydantic import BaseModel
from google import genai
from google.genai import types
from google.genai.errors import APIError

from app.core.config import settings
from app.providers.base import BaseLLMProvider


class GeminiProvider(BaseLLMProvider):
    """Google Gemini LLM provider implementation."""

    def __init__(self) -> None:
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY setting is required for GeminiProvider.")
        # Initialize the client (supports async via .aio)
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    async def generate_text(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7,
    ) -> str:
        try:
            config = types.GenerateContentConfig(
                temperature=temperature,
                system_instruction=system_instruction,
            )
            response = await self.client.aio.models.generate_content(
                model=settings.DEFAULT_MODEL,
                contents=prompt,
                config=config,
            )
            return response.text or ""
        except APIError as e:
            raise RuntimeError(f"Gemini API Error: {str(e)}") from e

    async def generate_structured(
        self,
        prompt: str,
        response_schema: Type[BaseModel],
        system_instruction: Optional[str] = None,
        temperature: float = 0.2,
    ) -> BaseModel:
        try:
            # We can pass the pydantic model schema directly
            config = types.GenerateContentConfig(
                temperature=temperature,
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=response_schema,
            )
            response = await self.client.aio.models.generate_content(
                model=settings.PREMIUM_MODEL,  # Use pro model for structured generation
                contents=prompt,
                config=config,
            )
            text_response = response.text or ""
            # Parse json into the response schema
            return response_schema.model_validate_json(text_response)
        except APIError as e:
            raise RuntimeError(f"Gemini API Error: {str(e)}") from e
        except Exception as e:
            raise RuntimeError(
                f"Failed to generate or parse structured output: {str(e)}"
            ) from e

    async def generate_embeddings(
        self,
        texts: Union[str, List[str]],
    ) -> List[List[float]]:
        try:
            contents = [texts] if isinstance(texts, str) else texts
            response = await self.client.aio.models.embed_content(
                model=settings.EMBEDDING_MODEL,
                contents=contents,
            )
            # Extract embedding vectors
            embeddings = [emb.values for emb in response.embeddings]
            return embeddings
        except APIError as e:
            raise RuntimeError(f"Gemini API Error: {str(e)}") from e
