import uuid
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from app.core.constants import TENANT_HEADER
from app.core.logging import get_logger

logger = get_logger(__name__)


class TenantMiddleware(BaseHTTPMiddleware):
    """Middleware that isolates requests by enforcing tenant organization identifier."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Exempt routes
        path = request.url.path 
        if (
            path == "/"
            or path == "/favicon.ico"
            or path.startswith("/docs")
            or "openapi.json" in path
            or path.startswith("/redoc")
            or "/auth" in path
            or "/health" in path
        ):
            return await call_next(request)

        tenant_id_str = request.headers.get(TENANT_HEADER)

        if not tenant_id_str:
            # Let the authentication dependencies handle missing tenant or return error directly
            logger.warning("Tenant identifier missing from request headers", path=path)
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": f"Missing required multi-tenant header: {TENANT_HEADER}"},
            )

        try:
            organization_id = int(tenant_id_str)
            request.state.organization_id = organization_id
        except (ValueError, TypeError):
            logger.error("Invalid Integer format in tenant header", header=tenant_id_str)
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": f"Invalid format for tenant header {TENANT_HEADER}. Must be an integer."},
            )

        response = await call_next(request)
        return response
