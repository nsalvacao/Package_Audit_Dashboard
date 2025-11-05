"""Rate limiting middleware for API protection."""
from __future__ import annotations

import time
from collections import defaultdict
from threading import Lock
from typing import Callable

from fastapi import HTTPException, Request, Response, status

from app.core.logging import get_logger

logger = get_logger(__name__)


class RateLimiter:
    """
    Simple in-memory rate limiter using token bucket algorithm.

    For production use with multiple workers, consider using Redis-based rate limiting.
    """

    def __init__(
        self,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000,
    ):
        """
        Initialize rate limiter.

        Args:
            requests_per_minute: Maximum requests per minute per IP
            requests_per_hour: Maximum requests per hour per IP
        """
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour

        # Storage: {ip: {minute: [(timestamp, count)], hour: [(timestamp, count)]}}
        self._storage: dict[str, dict[str, list[tuple[float, int]]]] = defaultdict(
            lambda: {"minute": [], "hour": []}
        )
        self._lock = Lock()

    def _clean_old_entries(self, entries: list[tuple[float, int]], window: float) -> list[tuple[float, int]]:
        """
        Remove entries older than the time window.

        Args:
            entries: List of (timestamp, count) tuples
            window: Time window in seconds

        Returns:
            Cleaned list of entries
        """
        current_time = time.time()
        return [(ts, count) for ts, count in entries if current_time - ts < window]

    def is_allowed(self, client_ip: str, path: str) -> tuple[bool, dict]:
        """
        Check if request from client IP is allowed.

        Args:
            client_ip: Client IP address
            path: Request path

        Returns:
            Tuple of (allowed, info_dict)
            info_dict contains: remaining, reset_at, limit
        """
        current_time = time.time()

        with self._lock:
            # Get client's request history
            client_data = self._storage[client_ip]

            # Clean old entries
            client_data["minute"] = self._clean_old_entries(client_data["minute"], 60)
            client_data["hour"] = self._clean_old_entries(client_data["hour"], 3600)

            # Count recent requests
            minute_count = sum(count for _, count in client_data["minute"])
            hour_count = sum(count for _, count in client_data["hour"])

            # Check limits
            if minute_count >= self.requests_per_minute:
                logger.warning(
                    f"Rate limit exceeded for {client_ip}",
                    client_ip=client_ip,
                    path=path,
                    limit_type="minute",
                    count=minute_count,
                )
                return False, {
                    "remaining": 0,
                    "reset_at": int(current_time + 60),
                    "limit": self.requests_per_minute,
                    "limit_type": "minute",
                }

            if hour_count >= self.requests_per_hour:
                logger.warning(
                    f"Rate limit exceeded for {client_ip}",
                    client_ip=client_ip,
                    path=path,
                    limit_type="hour",
                    count=hour_count,
                )
                return False, {
                    "remaining": 0,
                    "reset_at": int(current_time + 3600),
                    "limit": self.requests_per_hour,
                    "limit_type": "hour",
                }

            # Allow request and increment counters
            client_data["minute"].append((current_time, 1))
            client_data["hour"].append((current_time, 1))

            return True, {
                "remaining_minute": self.requests_per_minute - minute_count - 1,
                "remaining_hour": self.requests_per_hour - hour_count - 1,
                "reset_at_minute": int(current_time + 60),
                "reset_at_hour": int(current_time + 3600),
            }

    def get_client_ip(self, request: Request) -> str:
        """
        Extract client IP address from request.

        Checks X-Forwarded-For header for proxied requests.

        Args:
            request: FastAPI request object

        Returns:
            Client IP address
        """
        # Check for proxy headers
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # Take first IP if multiple
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        # Fallback to direct connection
        if request.client:
            return request.client.host

        return "unknown"


# Global rate limiter instance
_rate_limiter: RateLimiter | None = None


def get_rate_limiter() -> RateLimiter:
    """
    Get or create global rate limiter instance.

    Returns:
        RateLimiter instance
    """
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter(
            requests_per_minute=60,
            requests_per_hour=1000,
        )
    return _rate_limiter


async def rate_limit_middleware(request: Request, call_next: Callable) -> Response:
    """
    Middleware to enforce rate limiting on all requests.

    Args:
        request: FastAPI request
        call_next: Next middleware/handler in chain

    Returns:
        Response

    Raises:
        HTTPException: 429 if rate limit exceeded
    """
    limiter = get_rate_limiter()

    # Skip rate limiting for health checks
    if request.url.path.startswith("/health"):
        return await call_next(request)

    # Get client IP
    client_ip = limiter.get_client_ip(request)

    # Check rate limit
    allowed, info = limiter.is_allowed(client_ip, request.url.path)

    if not allowed:
        # Rate limit exceeded
        logger.warning(
            f"Rate limit exceeded: {client_ip} - {request.method} {request.url.path}",
            client_ip=client_ip,
            method=request.method,
            path=request.url.path,
            limit_type=info.get("limit_type"),
        )

        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "Rate limit exceeded",
                "limit": info["limit"],
                "limit_type": info["limit_type"],
                "reset_at": info["reset_at"],
                "message": f"Too many requests. Limit: {info['limit']} requests per {info['limit_type']}. Try again after {info['reset_at']}.",
            },
        )

    # Process request
    response = await call_next(request)

    # Add rate limit headers
    response.headers["X-RateLimit-Remaining-Minute"] = str(info.get("remaining_minute", 0))
    response.headers["X-RateLimit-Remaining-Hour"] = str(info.get("remaining_hour", 0))
    response.headers["X-RateLimit-Reset-Minute"] = str(info.get("reset_at_minute", 0))
    response.headers["X-RateLimit-Reset-Hour"] = str(info.get("reset_at_hour", 0))

    return response


# Path-specific rate limits (for sensitive operations)
class PathRateLimiter:
    """
    Rate limiter for specific paths with custom limits.
    """

    def __init__(self):
        """Initialize path-specific rate limiter."""
        self.path_limits = {
            # Expensive operations - lower limits
            "/api/advanced/*/vulnerabilities": (10, 100),  # 10/min, 100/hour
            "/api/advanced/*/dependency-tree": (10, 100),
            "/api/advanced/*/batch-uninstall": (5, 50),
            "/api/advanced/*/rollback/*": (5, 50),
            # Streaming endpoints - moderate limits
            "/api/streaming/*/*/uninstall": (20, 200),
            # Discovery and listing - higher limits
            "/api/discover": (30, 300),
            "/api/managers": (60, 1000),
        }
        self._limiters: dict[str, RateLimiter] = {}

    def get_limiter_for_path(self, path: str) -> RateLimiter | None:
        """
        Get rate limiter for specific path pattern.

        Args:
            path: Request path

        Returns:
            RateLimiter instance or None if no custom limit
        """
        for pattern, (per_min, per_hour) in self.path_limits.items():
            # Simple pattern matching (replace * with wildcard)
            if self._matches_pattern(path, pattern):
                key = f"{per_min}_{per_hour}"
                if key not in self._limiters:
                    self._limiters[key] = RateLimiter(
                        requests_per_minute=per_min,
                        requests_per_hour=per_hour,
                    )
                return self._limiters[key]
        return None

    def _matches_pattern(self, path: str, pattern: str) -> bool:
        """
        Simple pattern matching.

        Args:
            path: Actual path
            pattern: Pattern with * wildcards

        Returns:
            True if path matches pattern
        """
        import re

        regex_pattern = pattern.replace("*", "[^/]+")
        regex_pattern = f"^{regex_pattern}$"
        return bool(re.match(regex_pattern, path))
