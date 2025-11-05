"""Router responsável por expor informação dos gestores detectados."""
from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter

from app.adapters import BaseAdapter, get_registered_adapters

router = APIRouter(prefix="/api/managers", tags=["managers"])


def _capabilities(adapter: BaseAdapter) -> List[str]:
    return ["list_packages", "uninstall", "export_manifest"]


@router.get("", summary="Lista gestores de pacotes disponíveis")
async def list_managers() -> Dict[str, List[Dict[str, Any]]]:
    managers: List[Dict[str, Any]] = []

    for adapter_cls in get_registered_adapters():
        if adapter_cls.detect():
            version = adapter_cls.get_version()
            managers.append(
                {
                    "id": adapter_cls.manager_id,
                    "name": adapter_cls.display_name,
                    "version": version or "unknown",
                    "capabilities": _capabilities(adapter_cls),
                }
            )

    return {"managers": managers}
