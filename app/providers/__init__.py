# app/providers/__init__.py
from app.core.config import settings
from app.providers.base import BaseLLMProvider
from app.providers.gemini_provider import GeminiProvider
from app.providers.ollama_provider import OllamaProvider
from app.providers.openai_provider import OpenAIProvider
from app.providers.claude_provider import ClaudeProvider


PROVIDERS = {   
    "gemini": GeminiProvider,
    "openai": OpenAIProvider,
    "claude": ClaudeProvider,
    "ollama": OllamaProvider,
}


def _get_provider(provider_name: str) -> BaseLLMProvider:
    provider_class = PROVIDERS.get(provider_name.lower())

    if not provider_class:
        raise ValueError(
            f"Unsupported provider: {provider_name}. "
            f"Supported providers: {', '.join(PROVIDERS.keys())}"
        )

    return provider_class()


def get_provider() -> BaseLLMProvider:
    """Instantiate the active LLM provider based on settings."""
    return _get_provider(settings.LLM_PROVIDER)


def get_embedding_provider() -> BaseLLMProvider:
    """Instantiate the active embedding provider based on settings."""
    return _get_provider(settings.EMBEDDING_PROVIDER)