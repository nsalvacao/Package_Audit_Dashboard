"""Router para operações sobre pacotes (uninstall, etc.)."""
from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict

from fastapi import APIRouter, HTTPException, status

from app.adapters import get_adapter_by_id
from app.analysis import SnapshotManager
from app.core.locking import OperationInProgressError
from app.core.queue import OperationType, OperationQueue, get_operation_queue
from app.core.validation import InvalidPackageNameError, ValidationLayer

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/managers", tags=["packages"])


async def _run_in_thread(func, *args, **kwargs):
    return await asyncio.to_thread(func, *args, **kwargs)


@router.delete(
    "/{manager_id}/packages/{package_name}",
    summary="Desinstala pacote através do gestor indicado",
)
async def uninstall_package(
    manager_id: str,
    package_name: str,
    force: bool = False,
) -> Dict[str, Any]:
    try:
        clean_manager_id = ValidationLayer.sanitize_manager_id(manager_id)
    except InvalidPackageNameError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    try:
        clean_package_name = ValidationLayer.sanitize_package_name(package_name)
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
            detail=f"Gestor {clean_manager_id} não encontrado.",
        )

    adapter = adapter_cls()
    snapshot_manager = SnapshotManager()
    operation_queue: OperationQueue = get_operation_queue()
    operation_id = f"uninstall:{clean_manager_id}:{clean_package_name}"

    async def perform_uninstall():
        packages = await _run_in_thread(adapter.list_packages)
        snapshot = await _run_in_thread(
            snapshot_manager.create_snapshot,
            {clean_manager_id: packages},
            {"reason": "pre-uninstall", "package": clean_package_name},
        )
        result = await _run_in_thread(adapter.uninstall, clean_package_name, force)
        return snapshot, result

    try:
        snapshot_summary, uninstall_result = await operation_queue.execute(
            operation_id,
            OperationType.MUTATION,
            perform_uninstall,
        )
    except OperationInProgressError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    response = {
        "manager": clean_manager_id,
        "package": clean_package_name,
        "force": force,
        "success": uninstall_result.get("success", False),
        "snapshot_id": snapshot_summary.id if snapshot_summary else None,
        "snapshot_created_at": snapshot_summary.created_at if snapshot_summary else None,
        "command": {
            "stdout": uninstall_result.get("stdout"),
            "stderr": uninstall_result.get("stderr"),
            "returncode": uninstall_result.get("returncode"),
        },
    }
    return response
