"""Router para operações com streaming em tempo real (SSE)."""
from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, AsyncGenerator, Dict

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from app.adapters import get_adapter_by_id
from app.analysis import SnapshotManager
from app.core.locking import OperationInProgressError
from app.core.queue import OperationType, OperationQueue, get_operation_queue
from app.core.validation import InvalidPackageNameError, ValidationLayer

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/streaming", tags=["streaming"])


async def _run_in_thread(func, *args, **kwargs):
    return await asyncio.to_thread(func, *args, **kwargs)


async def event_generator(
    manager_id: str,
    package_name: str,
    force: bool = False,
) -> AsyncGenerator[str, None]:
    """Generator para eventos SSE durante operação de uninstall."""
    try:
        yield f"event: start\ndata: {json.dumps({'timestamp': datetime.now().isoformat(), 'status': 'starting'})}\n\n"

        clean_manager_id = ValidationLayer.sanitize_manager_id(manager_id)
        clean_package_name = ValidationLayer.sanitize_package_name(package_name)

        yield f"event: log\ndata: {json.dumps({'message': f'Validating manager: {clean_manager_id}'})}\n\n"

        adapter_cls = get_adapter_by_id(clean_manager_id)
        if adapter_cls is None:
            yield f"event: error\ndata: {json.dumps({'error': f'Manager {clean_manager_id} not supported'})}\n\n"
            return

        if not adapter_cls.detect():
            yield f"event: error\ndata: {json.dumps({'error': f'Manager {clean_manager_id} not found'})}\n\n"
            return

        adapter = adapter_cls()
        snapshot_manager = SnapshotManager()
        operation_queue: OperationQueue = get_operation_queue()
        operation_id = f"uninstall:{clean_manager_id}:{clean_package_name}"

        yield f"event: log\ndata: {json.dumps({'message': 'Creating snapshot...'})}\n\n"

        async def perform_uninstall():
            packages = await _run_in_thread(adapter.list_packages)
            snapshot = await _run_in_thread(
                snapshot_manager.create_snapshot,
                {clean_manager_id: packages},
                {"reason": "pre-uninstall", "package": clean_package_name},
            )
            yield f"event: snapshot\ndata: {json.dumps({'snapshot_id': snapshot.id if snapshot else None})}\n\n"

            yield f"event: log\ndata: {json.dumps({'message': f'Uninstalling {clean_package_name}...'})}\n\n"

            result = await _run_in_thread(adapter.uninstall, clean_package_name, force)
            return snapshot, result

        try:
            async for event in perform_uninstall():
                yield event
        except OperationInProgressError as exc:
            yield f"event: error\ndata: {json.dumps({'error': str(exc)})}\n\n"
            return

        yield f"event: complete\ndata: {json.dumps({'status': 'completed', 'timestamp': datetime.now().isoformat()})}\n\n"

    except InvalidPackageNameError as exc:
        yield f"event: error\ndata: {json.dumps({'error': str(exc)})}\n\n"
    except Exception as exc:
        logger.exception("Error in event generator")
        yield f"event: error\ndata: {json.dumps({'error': str(exc)})}\n\n"


@router.get(
    "/{manager_id}/packages/{package_name}/uninstall",
    summary="Desinstala pacote com streaming em tempo real (SSE)",
)
async def uninstall_package_stream(
    manager_id: str,
    package_name: str,
    force: bool = False,
):
    """Endpoint SSE para uninstall com logs em tempo real."""
    return StreamingResponse(
        event_generator(manager_id, package_name, force),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
