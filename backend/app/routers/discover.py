"""Router responsável por detetar gestores de pacotes disponíveis."""
from __future__ import annotations

from typing import Dict, List, Type

from fastapi import APIRouter

from app.adapters import BaseAdapter, get_registered_adapters

router = APIRouter(prefix="/api/discover", tags=["discover"])


def _available_adapters() -> List[Type[BaseAdapter]]:
    """Lista de adapters analisados durante a descoberta."""
    return get_registered_adapters()


@router.post("", summary="Detecta gestores instalados")
async def discover_managers() -> Dict[str, List[Dict[str, str]]]:
    """Deteta gestores suportados e retorna metadados base."""
    detected: List[Dict[str, str]] = []

    for adapter_cls in _available_adapters():
        if adapter_cls.detect():
            version = adapter_cls.get_version()
            detected.append(
                {
                    "id": adapter_cls.manager_id,
                    "name": adapter_cls.display_name,
                    "version": version or "unknown",
                }
            )

    return {"managers": detected}
