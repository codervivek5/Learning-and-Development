import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from app.core.logging import get_logger

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware logging HTTP request metadata and execution latency."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.time()
        path = request.url.path
        method = request.method

        logger.info("Incoming request", path=path, method=method, client_ip=request.client.host if request.client else None)

        try:
            response = await call_next(request)
            duration = time.time() - start_time
            logger.info(
                "Request completed",
                path=path,
                method=method,
                status_code=response.status_code,
                duration_ms=round(duration * 1000, 2),
            )
            return response
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                "Request failed",
                path=path,
                method=method,
                error=str(e),
                duration_ms=round(duration * 1000, 2),
            )
            raise e
