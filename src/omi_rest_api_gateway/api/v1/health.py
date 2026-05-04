from fastapi import APIRouter, Request

from omi_rest_api_gateway.core.config import Settings
from omi_rest_api_gateway.schemas.common import HealthResponse

router = APIRouter()


@router.get("/health/live", response_model=HealthResponse)
async def liveness(request: Request) -> HealthResponse:
    settings: Settings = request.app.state.settings
    return HealthResponse(
        status="ok",
        service=settings.api.title,
        version=settings.api.version,
        environment=settings.environment,
    )


@router.get("/health/ready", response_model=HealthResponse)
async def readiness(request: Request) -> HealthResponse:
    settings: Settings = request.app.state.settings
    return HealthResponse(
        status="ok",
        service=settings.api.title,
        version=settings.api.version,
        environment=settings.environment,
    )
