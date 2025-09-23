from fastapi import APIRouter

from app.api.v1.endpoints import health, metrics

router = APIRouter()

# Include endpoint routers
router.include_router(health.router, tags=['health'])
router.include_router(metrics.router, tags=['metrics'])
