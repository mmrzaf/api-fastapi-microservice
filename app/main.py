import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router
from app.api.exception_handlers import exception_handlers
from app.core.config import get_settings
from app.core.lifecycle import lifespan
from app.core.logging import setup_logging
from app.core.metrics import init_metrics, metrics_middleware

setup_logging()
logger = structlog.get_logger(__name__)

settings = get_settings()

app = FastAPI(
	title=settings.app_name,
	version=settings.app_version,
	debug=settings.debug,
	lifespan=lifespan,
)

init_metrics(settings.app_name, settings.app_version)

app.middleware('http')(metrics_middleware)

for exc_type, handler in exception_handlers.items():
	app.add_exception_handler(exc_type, handler)

if settings.cors_origins:
	app.add_middleware(
		CORSMiddleware,
		allow_origins=settings.cors_origins,
		allow_credentials=settings.cors_credentials,
		allow_methods=settings.cors_methods,
		allow_headers=settings.cors_headers,
	)

app.include_router(router, prefix=settings.api_prefix)


@app.get('/')
async def root():
	"""Root endpoint with comprehensive service information."""
	return {
		'service': settings.app_name,
		'version': settings.app_version,
		'status': 'running',
		'api': {'docs': '/docs', 'redoc': '/redoc', 'openapi': '/openapi.json'},
		'monitoring': {
			'health': f'{settings.api_prefix}/health',
			'metrics': f'{settings.api_prefix}/metrics',
		},
		'environment': {'debug': settings.debug, 'log_level': settings.log_level},
	}
