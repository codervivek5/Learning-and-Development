# app/providers/gemini_provider.py
import json
from typing import List, Optional, Type, Union

from google import genai
from google.genai import types
from google.genai.errors import APIError
from pydantic import BaseModel

from app.core.config import settings
from app.providers.base import BaseLLMProvider
from app.providers.ollama_provider import OllamaProvider


class GeminiProvider(BaseLLMProvider):
    """Google Gemini LLM provider implementation."""

    def __init__(self) -> None:
        if not settings.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY setting is required for GeminiProvider."
            )

        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    @staticmethod
    def _should_fallback_to_ollama(error: APIError) -> bool:
        """Determine whether Gemini errors should trigger Ollama fallback."""
        if error.code == 429:
            return True

        response_json = getattr(error, "response_json", None)

        if isinstance(response_json, dict):
            error_details = response_json.get("error", {})
            status = error_details.get("status")

            if status == "RESOURCE_EXHAUSTED":
                return True

        message = str(error)

        return (
            "RESOURCE_EXHAUSTED" in message
            or "quota" in message.lower()
        )

    @staticmethod
    def _get_fallback_provider() -> OllamaProvider:
        """Return configured fallback provider."""
        if not settings.OLLAMA_MODEL:
            raise RuntimeError(
                "Gemini fallback requested but OLLAMA_MODEL is not configured."
            )

        return OllamaProvider()

    async def _fallback_to_ollama_text(
        self,
        prompt: str,
        system_instruction: Optional[str],
        temperature: float,
    ) -> str:
        provider = self._get_fallback_provider()

        return await provider.generate_text(
            prompt=prompt,
            system_instruction=system_instruction,
            temperature=temperature,
        )

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

            if not response.text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return response.text

        except APIError as e:
            if self._should_fallback_to_ollama(e):
                return await self._fallback_to_ollama_text(
                    prompt=prompt,
                    system_instruction=system_instruction,
                    temperature=temperature,
                )

            raise RuntimeError(
                f"Gemini API Error: {str(e)}"
            ) from e

    async def generate_structured(
        self,
        prompt: str,
        response_schema: Type[BaseModel],
        system_instruction: Optional[str] = None,
        temperature: float = 0.2,
    ) -> BaseModel:
        try:
            config = types.GenerateContentConfig(
                temperature=temperature,
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=response_schema,
            )

            response = await self.client.aio.models.generate_content(
                model=settings.PREMIUM_MODEL,
                contents=prompt,
                config=config,
            )

            if not response.text:
                raise RuntimeError(
                    "Gemini returned an empty structured response."
                )

            try:
                return response_schema.model_validate_json(response.text)
            except Exception as e:
                try:
                    parsed = json.loads(response.text)
                except json.JSONDecodeError:
                    raise RuntimeError(
                        f"Gemini structured output was not valid JSON: {str(e)}. Raw output: {response.text}"
                    ) from e

                normalized = BaseLLMProvider._normalize_structured_payload(
                    parsed, response_schema
                )
                try:
                    return response_schema.model_validate(normalized)
                except Exception as e2:
                    raise RuntimeError(
                        f"Gemini structured output was not valid JSON: {str(e2)}. Raw output: {response.text}"
                    ) from e2

        except APIError as e:
            if self._should_fallback_to_ollama(e):
                provider = self._get_fallback_provider()

                return await provider.generate_structured(
                    prompt=prompt,
                    response_schema=response_schema,
                    system_instruction=system_instruction,
                    temperature=temperature,
                )

            raise RuntimeError(
                f"Gemini API Error: {str(e)}"
            ) from e

        except Exception as e:
            raise RuntimeError(
                f"Failed to generate structured output: {str(e)}"
            ) from e

    async def generate_embeddings(
        self,
        texts: Union[str, List[str]],
    ) -> List[List[float]]:
        try:
            if isinstance(texts, str):
                contents = [texts]
            else:
                contents = texts

            if not contents:
                raise ValueError(
                    "Input texts cannot be empty."
                )

            response = await self.client.aio.models.embed_content(
                model=settings.EMBEDDING_MODEL,
                contents=contents,
            )

            return [
                embedding.values
                for embedding in response.embeddings
            ]

        except APIError as e:
            raise RuntimeError(
                f"Gemini API Error: {str(e)}"
            ) from e