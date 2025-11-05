"""Router para health checks e status da API."""
from __future__ import annotations

import platform
from datetime import datetime, timezone
from typing import Dict, Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/health", tags=["health"])


@router.get("", summary="Health check endpoint")
async def health_check() -> Dict[str, Any]:
    """
    Verifica o estado de saúde da API.

    Returns informações sobre:
    - Status da aplicação
    - Versão
    - Uptime
    - Informações do sistema
    """
    return {
        "status": "healthy",
        "version": "0.1.0",
        "phase": "MVP Phase 1",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "system": {
            "platform": platform.system(),
            "python_version": platform.python_version(),
        },
    }


@router.get("/ready", summary="Readiness probe")
async def readiness_check() -> Dict[str, bool]:
    """
    Verifica se a aplicação está pronta para receber requests.
    Útil para Kubernetes readiness probes.
    """
    # TODO: Adicionar verificações de dependências (DB, storage, etc.)
    return {"ready": True}


@router.get("/live", summary="Liveness probe")
async def liveness_check() -> Dict[str, bool]:
    """
    Verifica se a aplicação está viva.
    Útil para Kubernetes liveness probes.
    """
    return {"alive": True}
