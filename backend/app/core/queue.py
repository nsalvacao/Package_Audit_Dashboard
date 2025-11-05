"""Fila de operações que garante serialização de mutações."""
from __future__ import annotations

from enum import Enum
from typing import Any, Callable, Coroutine

from app.core.locking import (
    LockManager,
    OperationInProgressError,
    get_lock_manager,
)


class OperationType(Enum):
    READ = "read"
    MUTATION = "mutation"


class OperationQueue:
    """Executa operações respeitando a distinção read/mutation."""

    def __init__(self, lock_manager: LockManager | None = None) -> None:
        self.lock_manager = lock_manager or get_lock_manager()

    async def execute(
        self,
        operation_id: str,
        operation_type: OperationType,
        func: Callable[..., Coroutine[Any, Any, Any]],
        *args,
        **kwargs,
    ) -> Any:
        if operation_type == OperationType.READ:
            return await func(*args, **kwargs)

        if not self.lock_manager.acquire_lock(operation_id):
            lock_info = self.lock_manager.get_lock_info() or {}
            blocker = lock_info.get("operation", "unknown")
            raise OperationInProgressError(
                f"Operation blocked by: {blocker}"
            )

        try:
            return await func(*args, **kwargs)
        finally:
            self.lock_manager.release_lock()


_queue: OperationQueue | None = None


def get_operation_queue() -> OperationQueue:
    global _queue
    if _queue is None:
        _queue = OperationQueue()
    return _queue
