from app.core.config import settings
from app.providers.base import BaseLLMProvider
from app.providers.gemini_provider import GeminiProvider
from app.providers.openai_provider import OpenAIProvider
from app.providers.claude_provider import ClaudeProvider


def get_provider() -> BaseLLMProvider:
    """Instantiate the active LLM provider based on settings."""
    provider_name = settings.LLM_PROVIDER.lower()
    if provider_name == "gemini":
        return GeminiProvider()
    elif provider_name == "openai":
        return OpenAIProvider()
    elif provider_name == "claude":
        return ClaudeProvider()
    else:
        raise ValueError(
            f"Unsupported LLM_PROVIDER: {provider_name}. "
            f"Please set LLM_PROVIDER to 'gemini'."
        )
