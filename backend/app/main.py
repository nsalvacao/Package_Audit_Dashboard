"""Aplicação FastAPI principal do Package Audit Dashboard."""
from __future__ import annotations

import os
import time
from contextlib import asynccontextmanager
from typing import Callable

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.core.enhanced_logging import DetailedLoggingMiddleware
from app.core.logging import get_logger, log_request, setup_logging
from app.core.rate_limiter import rate_limit_middleware
from app.routers import advanced, discover, health, managers, packages, streaming

# Load environment variables from .env file
load_dotenv()

# Setup logging on module import
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", None)
JSON_LOGS = os.getenv("JSON_LOGS", "false").lower() == "true"
ENABLE_DETAILED_LOGGING = os.getenv("ENABLE_DETAILED_LOGGING", "false").lower() == "true"
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

setup_logging(
    log_level=LOG_LEVEL,
    json_format=JSON_LOGS,
    log_file=LOG_FILE,
    use_colors=True,
)

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle handler to log startup/shutdown."""
    logger.info(
        "Package Audit Dashboard API starting",
        version="0.2.0",
        log_level=LOG_LEVEL,
        json_logs=JSON_LOGS,
    )
    try:
        yield
    finally:
        logger.info("Package Audit Dashboard API shutting down")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Package Audit Dashboard API",
        version="0.2.0",
        description="API para descoberta e gestão de gestores de pacotes com funcionalidades avançadas.",
        lifespan=lifespan,
    )

    # Rate limiting middleware (first to reject quickly)
    @app.middleware("http")
    async def rate_limiting(request: Request, call_next: Callable) -> Response:
        """Apply rate limiting to all requests."""
        return await rate_limit_middleware(request, call_next)

    # Logging middleware - Enhanced or Basic
    if ENABLE_DETAILED_LOGGING:
        # Enhanced logging with request/response bodies, headers, etc.
        logger.info("Using DETAILED logging mode (captures request/response bodies)")
        app.add_middleware(
            DetailedLoggingMiddleware,
            log_request_body=True,
            log_response_body=True,
            log_headers=True,
            max_body_length=10000,
            exclude_paths=["/health", "/metrics"],
        )
    else:
        # Basic logging (lightweight)
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

    # CORS middleware (uses environment variable)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

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
