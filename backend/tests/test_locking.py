"""Testes para LockManager."""
from __future__ import annotations

import json
import time
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from app.core.locking import LockManager


@pytest.fixture
def lock_manager(tmp_path, monkeypatch):
    lock_file = tmp_path / ".lock"

    monkeypatch.setattr(LockManager, "LOCK_FILE", lock_file)
    manager = LockManager()

    yield manager

    manager.force_release()


class TestLockAcquisition:
    def test_acquire_lock_success(self, lock_manager):
        assert lock_manager.acquire_lock("op:test")
        assert lock_manager.is_locked()

    def test_acquire_lock_blocked(self, lock_manager):
        assert lock_manager.acquire_lock("op:first")
        assert not lock_manager.acquire_lock("op:second")

    def test_release_lock(self, lock_manager):
        lock_manager.acquire_lock("op:test")
        assert lock_manager.release_lock()
        assert not lock_manager.is_locked()

    def test_release_without_lock(self, lock_manager):
        assert not lock_manager.release_lock()

    def test_release_other_pid(self, lock_manager, monkeypatch):
        lock_manager.acquire_lock("op:test")
        info = lock_manager.get_lock_info()
        info["pid"] = 99999
        lock_manager.LOCK_FILE.write_text(json.dumps(info))
        assert not lock_manager.release_lock()
        lock_manager.force_release()


class TestStaleLock:
    def test_detect_stale_lock(self, lock_manager):
        lock_manager.acquire_lock("op:test")
        info = lock_manager.get_lock_info()
        old = datetime.now() - timedelta(seconds=lock_manager.TIMEOUT + 10)
        info["timestamp"] = old.isoformat()
        lock_manager.LOCK_FILE.write_text(json.dumps(info))
        assert lock_manager.is_stale()

    def test_acquire_over_stale_lock(self, lock_manager):
        stale_info = {
            "operation": "old",
            "pid": 999,
            "timestamp": (datetime.now() - timedelta(seconds=60)).isoformat(),
        }
        lock_manager.LOCK_FILE.write_text(json.dumps(stale_info))
        assert lock_manager.acquire_lock("new")


class TestLockInfo:
    def test_get_lock_info(self, lock_manager):
        lock_manager.acquire_lock("op:test")
        info = lock_manager.get_lock_info()
        assert info is not None
        assert info["operation"] == "op:test"
        assert "pid" in info
        assert "timestamp" in info

    def test_get_lock_info_when_not_locked(self, lock_manager):
        assert lock_manager.get_lock_info() is None


class TestWaitForLock:
    def test_wait_succeeds_immediately(self, lock_manager):
        assert lock_manager.wait_for_lock("op:test", max_wait=1)

    def test_wait_timeout(self, lock_manager):
        lock_manager.acquire_lock("op:hold")
        assert not lock_manager.wait_for_lock("op:blocked", max_wait=0.1, poll_interval=0.05)


class TestConcurrency:
    def test_sequential_operations(self, lock_manager):
        assert lock_manager.acquire_lock("op:1")
        lock_manager.release_lock()
        assert lock_manager.acquire_lock("op:2")
        lock_manager.release_lock()


class TestForceRelease:
    def test_force_release(self, lock_manager):
        lock_manager.acquire_lock("op:test")
        lock_manager.force_release()
        assert not lock_manager.is_locked()
