"""Router para funcionalidades avançadas (Phase 2)."""
from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.adapters import get_adapter_by_id
from app.analysis import SnapshotManager
from app.core.locking import OperationInProgressError
from app.core.queue import OperationType, OperationQueue, get_operation_queue
from app.core.validation import InvalidPackageNameError, ValidationLayer

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/advanced", tags=["advanced"])


async def _run_in_thread(func, *args, **kwargs):
    return await asyncio.to_thread(func, *args, **kwargs)


# --- Dependency Tree ---


@router.get(
    "/{manager_id}/dependency-tree",
    summary="Obtém árvore de dependências de todos os pacotes",
)
async def get_dependency_tree(manager_id: str):
    """Retorna a árvore de dependências do gestor."""
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
            detail=f"Manager {clean_manager_id} not supported.",
        )

    if not adapter_cls.detect():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Manager {clean_manager_id} not found.",
        )

    adapter = adapter_cls()
    result = await _run_in_thread(adapter.get_dependency_tree)
    return result


@router.get(
    "/{manager_id}/dependency-tree/{package_name}",
    summary="Obtém árvore de dependências de um pacote específico",
)
async def get_package_dependency_tree(manager_id: str, package_name: str):
    """Retorna a árvore de dependências de um pacote específico."""
    try:
        clean_manager_id = ValidationLayer.sanitize_manager_id(manager_id)
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
            detail=f"Manager {clean_manager_id} not supported.",
        )

    if not adapter_cls.detect():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Manager {clean_manager_id} not found.",
        )

    adapter = adapter_cls()
    result = await _run_in_thread(adapter.get_dependency_tree, clean_package_name)
    return result


# --- Vulnerability Scanning ---


@router.get(
    "/{manager_id}/vulnerabilities",
    summary="Escaneia vulnerabilidades nos pacotes instalados",
)
async def scan_vulnerabilities(manager_id: str):
    """Escaneia vulnerabilidades conhecidas no gestor."""
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
            detail=f"Manager {clean_manager_id} not supported.",
        )

    if not adapter_cls.detect():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Manager {clean_manager_id} not found.",
        )

    adapter = adapter_cls()
    result = await _run_in_thread(adapter.scan_vulnerabilities)
    return result


# --- Lock File Export ---


@router.get(
    "/{manager_id}/lockfile",
    summary="Exporta lockfile do gestor de pacotes",
)
async def export_lockfile(manager_id: str):
    """Exporta o lockfile/requirements do gestor."""
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
            detail=f"Manager {clean_manager_id} not supported.",
        )

    if not adapter_cls.detect():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Manager {clean_manager_id} not found.",
        )

    adapter = adapter_cls()
    result = await _run_in_thread(adapter.export_lockfile)
    return result


# --- Batch Operations ---


class BatchUninstallRequest(BaseModel):
    """Request model for batch uninstall."""

    packages: List[str]
    force: bool = False


class BatchUninstallResponse(BaseModel):
    """Response model for batch uninstall."""

    manager: str
    total: int
    succeeded: List[str]
    failed: List[Dict[str, Any]]
    snapshot_id: Optional[str]


@router.post(
    "/{manager_id}/batch-uninstall",
    summary="Desinstala múltiplos pacotes em batch",
    response_model=BatchUninstallResponse,
)
async def batch_uninstall(
    manager_id: str,
    request: BatchUninstallRequest,
) -> BatchUninstallResponse:
    """Desinstala múltiplos pacotes de uma só vez."""
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
            detail=f"Manager {clean_manager_id} not supported.",
        )

    if not adapter_cls.detect():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Manager {clean_manager_id} not found.",
        )

    adapter = adapter_cls()
    snapshot_manager = SnapshotManager()
    operation_queue: OperationQueue = get_operation_queue()

    # Sanitize all package names
    try:
        clean_packages = [
            ValidationLayer.sanitize_package_name(pkg) for pkg in request.packages
        ]
    except InvalidPackageNameError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid package name: {exc}",
        ) from exc

    # Create snapshot before batch operation
    packages_before = await _run_in_thread(adapter.list_packages)
    snapshot = await _run_in_thread(
        snapshot_manager.create_snapshot,
        {clean_manager_id: packages_before},
        {"reason": "pre-batch-uninstall", "packages": clean_packages},
    )

    succeeded = []
    failed = []

    # Execute uninstall for each package
    for package in clean_packages:
        operation_id = f"batch-uninstall:{clean_manager_id}:{package}"

        async def perform_uninstall():
            return await _run_in_thread(adapter.uninstall, package, request.force)

        try:
            result = await operation_queue.execute(
                operation_id,
                OperationType.MUTATION,
                perform_uninstall,
            )

            if result.get("success"):
                succeeded.append(package)
            else:
                failed.append(
                    {
                        "package": package,
                        "error": result.get("stderr", "Unknown error"),
                    }
                )

        except OperationInProgressError:
            failed.append(
                {
                    "package": package,
                    "error": "Operation already in progress",
                }
            )
        except Exception as exc:
            logger.exception("Failed to uninstall %s", package)
            failed.append(
                {
                    "package": package,
                    "error": str(exc),
                }
            )

    return BatchUninstallResponse(
        manager=clean_manager_id,
        total=len(clean_packages),
        succeeded=succeeded,
        failed=failed,
        snapshot_id=snapshot.id if snapshot else None,
    )


# --- Rollback ---


@router.post(
    "/{manager_id}/rollback/{snapshot_id}",
    summary="Faz rollback para um snapshot anterior",
)
async def rollback_to_snapshot(manager_id: str, snapshot_id: str):
    """Restaura o estado de um snapshot anterior."""
    try:
        clean_manager_id = ValidationLayer.sanitize_manager_id(manager_id)
    except InvalidPackageNameError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    snapshot_manager = SnapshotManager()

    # Load snapshot
    try:
        snapshot = await _run_in_thread(snapshot_manager.load_snapshot, snapshot_id)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Snapshot {snapshot_id} not found: {exc}",
        ) from exc

    # Get current state
    adapter_cls = get_adapter_by_id(clean_manager_id)
    if adapter_cls is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Manager {clean_manager_id} not supported.",
        )

    if not adapter_cls.detect():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Manager {clean_manager_id} not found.",
        )

    adapter = adapter_cls()
    current_packages = await _run_in_thread(adapter.list_packages)
    current_names = {pkg["name"] for pkg in current_packages}

    # Get snapshot packages for this manager
    snapshot_packages = snapshot.data.get(clean_manager_id, [])
    snapshot_names = {pkg["name"] for pkg in snapshot_packages}

    # Calculate differences
    to_uninstall = current_names - snapshot_names
    # Note: to_install would require package installation functionality

    results = {
        "snapshot_id": snapshot_id,
        "manager": clean_manager_id,
        "uninstalled": [],
        "failed": [],
        "note": "Only uninstall rollback is implemented. Install functionality needed for full rollback.",
    }

    # Uninstall packages that weren't in snapshot
    for package in to_uninstall:
        try:
            result = await _run_in_thread(adapter.uninstall, package, force=False)
            if result.get("success"):
                results["uninstalled"].append(package)
            else:
                results["failed"].append(
                    {"package": package, "error": result.get("stderr")}
                )
        except Exception as exc:
            logger.exception("Failed to uninstall %s during rollback", package)
            results["failed"].append({"package": package, "error": str(exc)})

    return results
