"""Router responsável por expor informação dos gestores detectados."""
from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, status

from app.adapters import BaseAdapter, get_adapter_by_id, get_registered_adapters

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


@router.get("/{manager_id}/packages", summary="Lista pacotes instalados")
async def list_packages(manager_id: str) -> Dict[str, Any]:
    """
    Lista todos os pacotes instalados por um gestor específico.

    Args:
        manager_id: ID do gestor (npm, pip, etc.)

    Returns:
        Lista de pacotes com nome e versão

    Raises:
        404: Gestor não encontrado ou não instalado
        500: Erro ao listar pacotes
    """
    adapter_cls = get_adapter_by_id(manager_id)

    if not adapter_cls:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Package manager '{manager_id}' not found",
        )

    if not adapter_cls.detect():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Package manager '{manager_id}' is not installed on this system",
        )

    try:
        adapter = adapter_cls()
        packages = adapter.list_packages()

        return {
            "manager_id": manager_id,
            "manager_name": adapter_cls.display_name,
            "total": len(packages),
            "packages": packages,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list packages: {str(e)}",
        )
