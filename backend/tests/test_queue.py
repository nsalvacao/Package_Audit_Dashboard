"""Testes para OperationQueue."""
from __future__ import annotations

import asyncio

import pytest

from app.core import locking
from app.core.locking import OperationInProgressError
from app.core.queue import (
    OperationQueue,
    OperationType,
    get_operation_queue,
)


@pytest.fixture
def isolated_queue(tmp_path, monkeypatch):
    monkeypatch.setattr(locking.LockManager, "LOCK_FILE", tmp_path / ".lock")
    locking._lock_manager = None  # reset singleton
    from app.core import queue as queue_module

    queue_module._queue = None
    manager = locking.get_lock_manager()
    operation_queue = OperationQueue(manager)
    yield operation_queue
    manager.force_release()
    queue_module._queue = None
    locking._lock_manager = None


@pytest.mark.asyncio
async def test_read_operations_run_without_lock(isolated_queue):
    results = []

    async def read_op(value):
        await asyncio.sleep(0)
        results.append(value)
        return value

    res = await asyncio.gather(
        isolated_queue.execute("read:1", OperationType.READ, read_op, 1),
        isolated_queue.execute("read:2", OperationType.READ, read_op, 2),
    )

    assert sorted(res) == [1, 2]
    assert sorted(results) == [1, 2]


@pytest.mark.asyncio
async def test_mutation_serialization(isolated_queue):
    start_event = asyncio.Event()
    finish_event = asyncio.Event()

    async def long_mutation():
        start_event.set()
        await finish_event.wait()
        return "done"

    task = asyncio.create_task(
        isolated_queue.execute(
            "mut:1",
            OperationType.MUTATION,
            long_mutation,
        )
    )

    await start_event.wait()

    with pytest.raises(OperationInProgressError):
        await isolated_queue.execute(
            "mut:2",
            OperationType.MUTATION,
            long_mutation,
        )

    finish_event.set()
    assert await task == "done"


@pytest.mark.asyncio
async def test_mutation_releases_lock_on_error(isolated_queue):
    async def failing_mutation():
        raise ValueError("boom")

    with pytest.raises(ValueError):
        await isolated_queue.execute(
            "mut:error",
            OperationType.MUTATION,
            failing_mutation,
        )

    async def succeeding():
        return "ok"

    assert await isolated_queue.execute(
        "mut:after-error",
        OperationType.MUTATION,
        succeeding,
    ) == "ok"


@pytest.mark.asyncio
async def test_get_operation_queue_singleton(tmp_path, monkeypatch):
    monkeypatch.setattr(locking.LockManager, "LOCK_FILE", tmp_path / ".lock")
    locking._lock_manager = None
    from app.core import queue as queue_module

    queue_module._queue = None
    try:
        q1 = get_operation_queue()
        q2 = get_operation_queue()
        assert q1 is q2
    finally:
        queue_module._queue = None
        locking._lock_manager = None
