from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from uuid import uuid4

import httpx
import structlog
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from omi_rest_api_gateway.api.router import api_router
from omi_rest_api_gateway.clients.omi import OmiPortalClient
from omi_rest_api_gateway.core.config import Settings, get_settings
from omi_rest_api_gateway.core.exceptions import register_exception_handlers
from omi_rest_api_gateway.core.logging import configure_logging

logger = structlog.get_logger(__name__)


def build_lifespan(settings: Settings) -> Callable[[FastAPI], AbstractAsyncContextManager[None]]:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        configure_logging(settings.log_level)

        timeout = httpx.Timeout(settings.omi.timeout_seconds)
        async with httpx.AsyncClient(
            base_url=str(settings.omi.base_url),
            timeout=timeout,
        ) as http_client:
            app.state.settings = settings
            app.state.omi_client = OmiPortalClient(http_client=http_client)
            logger.info("application_started", environment=settings.environment)
            yield
            logger.info("application_stopped")

    return lifespan


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved_settings = settings or get_settings()
    configure_logging(resolved_settings.log_level)

    app = FastAPI(
        title=resolved_settings.api.title,
        version=resolved_settings.api.version,
        description="REST API gateway for Italian OMI portal quotation data.",
        docs_url=resolved_settings.api.docs_url,
        redoc_url=resolved_settings.api.redoc_url,
        openapi_url=f"{resolved_settings.api.prefix}/openapi.json",
        lifespan=build_lifespan(resolved_settings),
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=resolved_settings.api.cors_origins,
        allow_credentials=resolved_settings.api.cors_allow_credentials,
        allow_methods=resolved_settings.api.cors_allow_methods,
        allow_headers=resolved_settings.api.cors_allow_headers,
    )

    @app.middleware("http")
    async def request_context_middleware(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request_id = request.headers.get("x-request-id", str(uuid4()))
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)
        response = await call_next(request)
        response.headers["x-request-id"] = request_id
        return response

    register_exception_handlers(app)
    app.include_router(api_router, prefix=resolved_settings.api.prefix)

    @app.get("/", include_in_schema=False)
    async def root() -> dict[str, str]:
        return {
            "name": resolved_settings.api.title,
            "version": resolved_settings.api.version,
            "docs": resolved_settings.api.docs_url or "",
        }

    return app


app = create_app()


def run() -> None:
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "omi_rest_api_gateway.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower(),
    )
