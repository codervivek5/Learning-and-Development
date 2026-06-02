import re
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from app.core.security import decode_token
from app.core.logging import get_logger

logger = get_logger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware that extracts and verifies JWT authorization header."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Exempt health checks, docs, and authentication paths
        path = request.url.path
        if (
            path.startswith("/docs")
            or path.startswith("/openapi.json")
            or path.startswith("/redoc")
            or "/auth" in path
            or "/health" in path
        ):
            return await call_next(request)

        request.state.user_id = None
        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            payload = decode_token(token)
            if payload and "sub" in payload:
                request.state.user_id = payload["sub"]
                logger.debug("AuthMiddleware attached user_id", user_id=payload["sub"])

        response = await call_next(request)
        return response
