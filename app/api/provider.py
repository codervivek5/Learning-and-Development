from typing import List

from fastapi import APIRouter, Form, HTTPException, status
from pydantic import ValidationError

from app.schemas.provider import (
    ProviderListResponse,
    ProviderName,
    ProviderResponse,
    ProviderUpdateRequest,
)
from app.services.provider_service import ProviderService

router = APIRouter()


@router.get("/providers", response_model=ProviderListResponse)
async def list_providers():
    providers = ProviderService.get_supported_providers()
    return ProviderListResponse(providers=providers)


@router.get("/providers/current", response_model=ProviderResponse)
async def get_current_provider():
    return ProviderService.get_current_provider()


@router.post("/providers/switch", response_model=ProviderResponse)
async def switch_provider(
    provider: ProviderName = Form(
        ...,
        description="Select the active AI model provider.",
    ),
):
    try:
        request = ProviderUpdateRequest(provider=provider)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors())

    return ProviderService.set_provider(request.provider)
