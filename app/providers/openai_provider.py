from typing import List, Optional, Type, Union
from pydantic import BaseModel
from app.providers.base import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):
    """Stub implementation for OpenAI provider."""

    def __init__(self) -> None:
        raise NotImplementedError(
            "OpenAIProvider is not implemented yet. Set LLM_PROVIDER=gemini."
        )

    async def generate_text(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7,
    ) -> str:
        raise NotImplementedError()

    async def generate_structured(
        self,
        prompt: str,
        response_schema: Type[BaseModel],
        system_instruction: Optional[str] = None,
        temperature: float = 0.2,
    ) -> BaseModel:
        raise NotImplementedError()

    async def generate_embeddings(
        self,
        texts: Union[str, List[str]],
    ) -> List[List[float]]:
        raise NotImplementedError()
