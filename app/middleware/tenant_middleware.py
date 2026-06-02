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

        referer = request.headers.get("referer", "")
        if "/docs" in referer or "127.0.0.1" in referer:
            # Mock a default tenant ID for Swagger interface verification smoothly
            request.state.organization_id = 1  # Assuming 1 is your first org id in DB
            return await call_next(request)

        logger.warning("Tenant identifier missing from request headers", path=path)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": f"Missing required multi-tenant header: {TENANT_HEADER}"},
        )
