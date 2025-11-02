import uuid

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class RequestContextMiddleware(BaseHTTPMiddleware):
	def __init__(self, app: ASGIApp):
		super().__init__(app)

	async def dispatch(self, request, call_next):
		rid = request.headers.get('x-request-id', str(uuid.uuid4()))
		request.state.request_id = rid
		structlog.contextvars.bind_contextvars(
			request_id=rid, path=request.url.path, method=request.method
		)
		try:
			return await call_next(request)
		finally:
			structlog.contextvars.clear_contextvars()
