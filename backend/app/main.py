"""Aplicação FastAPI principal do Package Audit Dashboard."""
from __future__ import annotations

import os
import time
from typing import Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging import get_logger, log_request, setup_logging
from app.core.rate_limiter import rate_limit_middleware
from app.routers import advanced, discover, health, managers, packages, streaming

# Setup logging on module import
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", None)
JSON_LOGS = os.getenv("JSON_LOGS", "false").lower() == "true"

setup_logging(
    log_level=LOG_LEVEL,
    json_format=JSON_LOGS,
    log_file=LOG_FILE,
    use_colors=True,
)

logger = get_logger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Package Audit Dashboard API",
        version="0.2.0",
        description="API para descoberta e gestão de gestores de pacotes com funcionalidades avançadas.",
    )

    # Rate limiting middleware (first to reject quickly)
    @app.middleware("http")
    async def rate_limiting(request: Request, call_next: Callable) -> Response:
        """Apply rate limiting to all requests."""
        return await rate_limit_middleware(request, call_next)

    # Request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next: Callable) -> Response:
        """Log all HTTP requests with timing."""
        start_time = time.time()

        # Process request
        response = await call_next(request)

        # Calculate duration
        duration_ms = (time.time() - start_time) * 1000

        # Log request
        log_request(
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
        )

        return response

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Startup event
    @app.on_event("startup")
    async def startup_event():
        """Log application startup."""
        logger.info(
            "Package Audit Dashboard API starting",
            version="0.2.0",
            log_level=LOG_LEVEL,
            json_logs=JSON_LOGS,
        )

    # Shutdown event
    @app.on_event("shutdown")
    async def shutdown_event():
        """Log application shutdown."""
        logger.info("Package Audit Dashboard API shutting down")

    # Health check endpoints (no /api prefix for standard health checks)
    app.include_router(health.router)

    # API endpoints
    app.include_router(discover.router)
    app.include_router(managers.router)
    app.include_router(packages.router)
    app.include_router(streaming.router)
    app.include_router(advanced.router)

    logger.info("Application initialized successfully")
    return app


app = create_app()
