from fastapi import FastAPI

from app.api import router as api_router
from app.api.exception_handlers import install_error_handlers
from app.core.config import get_settings
from app.core.lifecycle import lifespan
from app.core.middlewares import install_middleware

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs" if settings.app_env != "prd" else None,
    redoc_url="/redoc" if settings.app_env != "prd" else None,
    openapi_url="/openapi.json" if settings.app_env != "prd" else None,
)

install_middleware(app)
install_error_handlers(app)
app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/")
async def root():
    """Root endpoint for basic service visibility."""
    return {"service": settings.app_name, "version": settings.app_version, "status": "running"}
