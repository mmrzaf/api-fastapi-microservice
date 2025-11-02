from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.routes import router as v1
from app.core.errors import install_error_handlers
from app.core.middleware import install_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="My Starter",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

install_middleware(app)
install_error_handlers(app)
app.include_router(v1, prefix="/api/v1")
