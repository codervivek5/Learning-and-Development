from typing import List

from app.core.config import settings
from app.schemas.provider import ProviderName, ProviderResponse
from app.providers import PROVIDERS


class ProviderService:
    @staticmethod
    def get_supported_providers() -> List[ProviderName]:
        return [ProviderName(provider) for provider in PROVIDERS.keys()]

    @staticmethod
    def get_current_provider() -> ProviderResponse:
        return ProviderResponse(provider=ProviderName(settings.LLM_PROVIDER))

    @staticmethod
    def set_provider(provider: ProviderName) -> ProviderResponse:
        if provider.value not in PROVIDERS:
            raise ValueError(
                f"Unsupported provider: {provider}. Supported providers: {', '.join(PROVIDERS.keys())}"
            )
        settings.LLM_PROVIDER = provider.value
        return ProviderResponse(provider=provider)
