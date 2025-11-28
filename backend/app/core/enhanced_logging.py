"""Enhanced logging middleware for comprehensive debugging and analysis."""
from __future__ import annotations

import json
import time
import traceback
from typing import Any, Callable, Dict, List, Optional, Set

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Message

from app.core.logging import get_logger

logger = get_logger(__name__)

# Sensitive headers and fields to redact
SENSITIVE_HEADERS: Set[str] = {
    "authorization",
    "cookie",
    "set-cookie",
    "x-api-key",
    "x-auth-token",
}

SENSITIVE_FIELDS: Set[str] = {
    "password",
    "token",
    "secret",
    "api_key",
    "apikey",
    "auth",
    "credential",
}


def sanitize_data(data: Any, redact_value: str = "***REDACTED***") -> Any:
    """
    Recursively sanitize sensitive data from logs.

    Args:
        data: Data to sanitize (dict, list, or primitive)
        redact_value: Value to replace sensitive data with

    Returns:
        Sanitized copy of data
    """
    if isinstance(data, dict):
        return {
            key: redact_value
            if key.lower() in SENSITIVE_FIELDS
            else sanitize_data(value, redact_value)
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [sanitize_data(item, redact_value) for item in data]
    else:
        return data


def sanitize_headers(headers: Dict[str, str]) -> Dict[str, str]:
    """
    Sanitize sensitive headers.

    Args:
        headers: Request or response headers

    Returns:
        Sanitized headers dict
    """
    return {
        key: "***REDACTED***" if key.lower() in SENSITIVE_HEADERS else value
        for key, value in headers.items()
    }


class DetailedLoggingMiddleware(BaseHTTPMiddleware):
    """
    Enhanced middleware for comprehensive request/response logging.

    Captures:
    - Request method, path, headers, query params, body
    - Response status, headers, body
    - Timing information
    - Error details with full stack traces
    """

    def __init__(
        self,
        app,
        log_request_body: bool = True,
        log_response_body: bool = True,
        log_headers: bool = True,
        max_body_length: int = 10000,
        exclude_paths: Optional[List[str]] = None,
    ):
        """
        Initialize the middleware.

        Args:
            app: FastAPI application
            log_request_body: Whether to log request bodies
            log_response_body: Whether to log response bodies
            log_headers: Whether to log headers
            max_body_length: Maximum body length to log (truncate after)
            exclude_paths: Paths to exclude from detailed logging (e.g., /health)
        """
        super().__init__(app)
        self.log_request_body = log_request_body
        self.log_response_body = log_response_body
        self.log_headers = log_headers
        self.max_body_length = max_body_length
        self.exclude_paths = exclude_paths or ["/health", "/metrics"]

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with detailed logging."""
        # Skip detailed logging for excluded paths
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            return await call_next(request)

        # Generate unique request ID
        request_id = f"{int(time.time() * 1000000)}"
        start_time = time.time()

        # Capture request details
        request_data = await self._capture_request(request, request_id)

        # Log incoming request
        logger.info(
            f"→ {request.method} {request.url.path}",
            request_id=request_id,
            **request_data,
        )

        # Store original body for error handling
        response_body = b""
        response_status = 200
        error_details = None

        try:
            # Process request and capture response
            response = await call_next(request)
            response_status = response.status_code

            # Capture response body if needed
            if self.log_response_body and response_status >= 400:
                response_body = await self._read_response_body(response)

            # Log response
            duration_ms = (time.time() - start_time) * 1000
            response_data = self._capture_response(
                response, response_body, duration_ms
            )

            log_level = "info" if response_status < 400 else "error"
            getattr(logger, log_level)(
                f"← {request.method} {request.url.path} {response_status}",
                request_id=request_id,
                duration_ms=round(duration_ms, 2),
                **response_data,
            )

            return response

        except Exception as exc:
            # Capture error details
            duration_ms = (time.time() - start_time) * 1000
            error_details = self._capture_error(exc)

            logger.error(
                f"✗ {request.method} {request.url.path} FAILED",
                request_id=request_id,
                duration_ms=round(duration_ms, 2),
                **error_details,
            )

            # Re-raise to let FastAPI handle it
            raise

    async def _capture_request(
        self, request: Request, request_id: str
    ) -> Dict[str, Any]:
        """
        Capture comprehensive request details.

        Args:
            request: FastAPI request object
            request_id: Unique request identifier

        Returns:
            Dict with request details
        """
        data: Dict[str, Any] = {
            "method": request.method,
            "path": request.url.path,
            "query_params": dict(request.query_params),
        }

        # Capture headers
        if self.log_headers:
            data["headers"] = sanitize_headers(dict(request.headers))

        # Capture request body
        if self.log_request_body and request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.body()
                if body:
                    try:
                        # Try to parse as JSON
                        body_data = json.loads(body)
                        sanitized_body = sanitize_data(body_data)
                        body_str = json.dumps(sanitized_body)
                    except json.JSONDecodeError:
                        # Fall back to string
                        body_str = body.decode("utf-8", errors="replace")

                    # Truncate if too long
                    if len(body_str) > self.max_body_length:
                        body_str = (
                            body_str[: self.max_body_length]
                            + f"... (truncated, total: {len(body_str)} chars)"
                        )

                    data["request_body"] = body_str
            except Exception as e:
                data["request_body_error"] = str(e)

        return data

    def _capture_response(
        self, response: Response, body: bytes, duration_ms: float
    ) -> Dict[str, Any]:
        """
        Capture response details.

        Args:
            response: Response object
            body: Response body bytes
            duration_ms: Request duration

        Returns:
            Dict with response details
        """
        data: Dict[str, Any] = {
            "status_code": response.status_code,
        }

        # Capture headers
        if self.log_headers:
            data["response_headers"] = sanitize_headers(dict(response.headers))

        # Capture response body for errors
        if body and response.status_code >= 400:
            try:
                body_str = body.decode("utf-8", errors="replace")
                if len(body_str) > self.max_body_length:
                    body_str = (
                        body_str[: self.max_body_length]
                        + f"... (truncated, total: {len(body_str)} chars)"
                    )
                data["response_body"] = body_str
            except Exception as e:
                data["response_body_error"] = str(e)

        return data

    def _capture_error(self, exc: Exception) -> Dict[str, Any]:
        """
        Capture comprehensive error details.

        Args:
            exc: Exception that occurred

        Returns:
            Dict with error details
        """
        return {
            "error_type": type(exc).__name__,
            "error_message": str(exc),
            "error_traceback": traceback.format_exc(),
            "error_args": exc.args,
        }

    async def _read_response_body(self, response: Response) -> bytes:
        """
        Read response body while preserving it for client.

        Args:
            response: Response object

        Returns:
            Response body as bytes
        """
        body = b""
        async for chunk in response.body_iterator:
            body += chunk

        # Create new response with same body
        async def new_body_iterator():
            yield body

        response.body_iterator = new_body_iterator()
        return body


class OperationLogger:
    """
    Context manager for logging operations with automatic timing and error handling.

    Usage:
        async with OperationLogger("uninstall_package", manager_id="npm", package="lodash"):
            # ... operation code ...
            pass
    """

    def __init__(
        self,
        operation_name: str,
        logger_name: str = "operations",
        **context: Any,
    ):
        """
        Initialize operation logger.

        Args:
            operation_name: Name of the operation
            logger_name: Logger name to use
            **context: Additional context to log
        """
        self.operation_name = operation_name
        self.logger = get_logger(logger_name)
        self.context = context
        self.start_time: Optional[float] = None
        self.success = False

    async def __aenter__(self):
        """Start operation logging."""
        self.start_time = time.time()
        self.logger.info(
            f"▶ Starting: {self.operation_name}",
            operation=self.operation_name,
            **self.context,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Complete operation logging."""
        duration_ms = (time.time() - self.start_time) * 1000 if self.start_time else 0
        self.success = exc_type is None

        if self.success:
            self.logger.info(
                f"✓ Completed: {self.operation_name}",
                operation=self.operation_name,
                success=True,
                duration_ms=round(duration_ms, 2),
                **self.context,
            )
        else:
            self.logger.error(
                f"✗ Failed: {self.operation_name}",
                operation=self.operation_name,
                success=False,
                duration_ms=round(duration_ms, 2),
                error_type=exc_type.__name__ if exc_type else None,
                error_message=str(exc_val) if exc_val else None,
                **self.context,
            )

        # Don't suppress exception
        return False

    def add_context(self, **kwargs: Any) -> None:
        """
        Add additional context during operation.

        Args:
            **kwargs: Context key-value pairs
        """
        self.context.update(kwargs)
