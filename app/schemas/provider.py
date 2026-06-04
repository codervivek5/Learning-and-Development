from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class ProviderName(str, Enum):
    gemini = "gemini"
    openai = "openai"
    claude = "claude"
    ollama = "ollama"


class ProviderUpdateRequest(BaseModel):
    provider: ProviderName = Field(
        ..., 
        description="Select one of the supported LLM providers.",
        example="gemini"
    )


class ProviderResponse(BaseModel):
    provider: ProviderName


class ProviderListResponse(BaseModel):
    providers: List[ProviderName]
