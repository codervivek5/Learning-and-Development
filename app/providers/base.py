# app/providers/base.py
import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type, Union
from pydantic import BaseModel


class BaseLLMProvider(ABC):
    """Abstract interface for multi-provider LLM support."""

    @staticmethod
    def _normalize_structured_payload(
        payload: Any,
        response_schema: Type[BaseModel],
    ) -> Any:
        if isinstance(payload, dict):
            normalized = {}
            for key, value in payload.items():
                field_info = response_schema.model_fields.get(key)
                field_annotation = str(field_info.annotation) if field_info else ""

                if isinstance(value, dict):
                    if "str" in field_annotation and "list" not in field_annotation.lower():
                        normalized[key] = json.dumps(value, ensure_ascii=False)
                    else:
                        normalized[key] = BaseLLMProvider._normalize_structured_payload(
                            value, response_schema
                        )
                elif isinstance(value, list):
                    list_type_hint = "list" in field_annotation.lower() or "typing.list" in field_annotation.lower()

                    if list_type_hint:
                        normalized[key] = [
                            BaseLLMProvider._normalize_structured_payload(item, response_schema)
                            for item in value
                        ]
                    elif "str" in field_annotation:
                        normalized[key] = json.dumps(value, ensure_ascii=False)
                    else:
                        normalized[key] = [
                            BaseLLMProvider._normalize_structured_payload(item, response_schema)
                            for item in value
                        ]
                else:
                    normalized[key] = value
            return normalized

        if isinstance(payload, list):
            return [
                BaseLLMProvider._normalize_structured_payload(item, response_schema)
                for item in payload
            ]

        return payload

    @abstractmethod
    async def generate_text(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7,
    ) -> str:
        """Generates plain text response."""
        pass

    @abstractmethod
    async def generate_structured(
        self,
        prompt: str,
        response_schema: Type[BaseModel],
        system_instruction: Optional[str] = None,
        temperature: float = 0.2,
    ) -> BaseModel:
        """Generates structured data validated by a Pydantic model."""
        pass

    @abstractmethod
    async def generate_embeddings(
        self,
        texts: Union[str, List[str]],
    ) -> List[List[float]]:
        """Generates vector embeddings for a given text or list of texts."""
        pass
