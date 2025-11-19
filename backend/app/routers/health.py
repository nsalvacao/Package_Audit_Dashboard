"""Health check router for monitoring and status checks."""
from __future__ import annotations

import platform
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/health", tags=["health"])


class HealthStatus(BaseModel):
    """Health check response model."""

    status: str
    timestamp: str
    version: str
    python_version: str
    platform: str
    uptime_seconds: Optional[float] = None


class DetailedHealthStatus(HealthStatus):
    """Detailed health check with additional system info."""

    package_managers: Dict[str, bool]
    storage_available: bool
    storage_path: str


# Store startup time for uptime calculation
_startup_time = datetime.now()


@router.get("", response_model=HealthStatus)
async def health_check() -> dict:
    """
    Basic health check endpoint.

    Returns:
        Simple health status with timestamp
    """
    current_time = datetime.now()
    uptime = (current_time - _startup_time).total_seconds()

    return {
        "status": "healthy",
        "timestamp": current_time.isoformat(),
        "version": "0.2.0",
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "platform": platform.system(),
        "uptime_seconds": uptime,
    }


@router.get("/detailed", response_model=DetailedHealthStatus)
async def detailed_health_check() -> dict:
    """
    Detailed health check with system information.

    Returns:
        Comprehensive health status including package manager availability
    """
    import shutil
    from app.adapters import BrewAdapter, NpmAdapter, PipAdapter, WingetAdapter

    current_time = datetime.now()
    uptime = (current_time - _startup_time).total_seconds()

    # Check package manager availability
    package_managers = {
        "npm": shutil.which("npm") is not None,
        "pip": shutil.which("pip") is not None or shutil.which("pip3") is not None,
        "brew": shutil.which("brew") is not None,
        "winget": shutil.which("winget") is not None,
    }

    # Check storage availability
    storage_path = Path.home() / ".package-audit"
    storage_available = True
    try:
        storage_path.mkdir(parents=True, exist_ok=True)
        storage_available = storage_path.exists() and storage_path.is_dir()
    except Exception:
        storage_available = False

    return {
        "status": "healthy",
        "timestamp": current_time.isoformat(),
        "version": "0.2.0",
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "platform": platform.system(),
        "uptime_seconds": uptime,
        "package_managers": package_managers,
        "storage_available": storage_available,
        "storage_path": str(storage_path),
    }


@router.get("/ready")
async def readiness_check() -> dict:
    """
    Kubernetes-style readiness probe.

    Returns:
        Simple ready status for container orchestration
    """
    return {"ready": True}


@router.get("/live")
async def liveness_check() -> dict:
    """
    Kubernetes-style liveness probe.

    Returns:
        Simple alive status for container orchestration
    """
    return {"alive": True}
