from fastapi import APIRouter

from omi_rest_api_gateway.api.v1.health import router as health_router
from omi_rest_api_gateway.api.v1.omi import router as omi_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(omi_router, prefix="/omi", tags=["omi"])
