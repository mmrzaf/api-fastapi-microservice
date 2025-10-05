import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from structlog import contextvars as ctx

class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        ctx.clear_contextvars()
        ctx.bind_contextvars(
            request_id=str(uuid.uuid4()),
            method=request.method,
            path=request.url.path,
            client_ip=request.client.host if request.client else None,
        )
        try:
            return await call_next(request)
        finally:
            ctx.clear_contextvars()
