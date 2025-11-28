"""Router responsável por expor informação dos gestores detectados."""
from __future__ import annotations

import logging
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, status

from app.adapters import BaseAdapter, get_adapter_by_id, get_registered_adapters
from app.core.validation import InvalidPackageNameError, ValidationLayer

logger = logging.getLogger(__name__)

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


@router.get("/{manager_id}/packages", summary="Lista pacotes instalados do gestor")
async def list_packages(manager_id: str) -> Dict[str, List[Dict[str, Any]]]:
    """Retorna lista de pacotes instalados através do gestor especificado."""
    try:
        clean_manager_id = ValidationLayer.sanitize_manager_id(manager_id)
    except InvalidPackageNameError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    adapter_cls = get_adapter_by_id(clean_manager_id)
    if adapter_cls is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gestor {clean_manager_id} não suportado.",
        )

    if not adapter_cls.detect():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gestor {clean_manager_id} não encontrado no sistema.",
        )

    adapter = adapter_cls()

    try:
        packages = adapter.list_packages()
        return {"packages": packages}
    except Exception as exc:
        logger.error(f"Erro ao listar pacotes do gestor {clean_manager_id}: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar pacotes: {str(exc)}",
        ) from exc
