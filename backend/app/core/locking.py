"""Gestor de locks baseado em ficheiro para serializar operações críticas."""
from __future__ import annotations

import atexit
import json
import os
import signal
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional


class OperationInProgressError(Exception):
    """Operação bloqueada por lock existente."""


class LockManager:
    """Controla exclusão mútua de operações de mutação."""

    LOCK_FILE = Path.home() / ".package-audit" / ".lock"
    TIMEOUT = 30  # segundos

    def __init__(self) -> None:
        self.LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
        atexit.register(self._cleanup_handler)
        self._register_signal(signal.SIGTERM)
        self._register_signal(signal.SIGINT)

    def _register_signal(self, sig) -> None:
        try:
            signal.signal(sig, self._signal_handler)
        except (AttributeError, ValueError):
            # A plataforma não suporta este sinal (ex.: Windows) ou estamos fora da main thread.
            pass

    def acquire_lock(self, operation_id: str) -> bool:
        if self.is_locked() and not self.is_stale():
            return False

        if self.is_stale():
            self.release_lock(force=True)

        lock_data = {
            "operation": operation_id,
            "pid": os.getpid(),
            "timestamp": datetime.now().isoformat(),
            "hostname": getattr(os, "uname", lambda: None)() .nodename
            if hasattr(os, "uname")
            else os.getenv("HOSTNAME", "unknown"),
        }

        try:
            with open(self.LOCK_FILE, "w", encoding="utf-8") as lock:
                json.dump(lock_data, lock, indent=2)
            return True
        except OSError:
            return False

    def release_lock(self, force: bool = False) -> bool:
        if not self.is_locked():
            return False

        try:
            lock_data = self.get_lock_info() or {}
            if force or lock_data.get("pid") == os.getpid():
                self.LOCK_FILE.unlink(missing_ok=True)
                return True
            return False
        except OSError:
            return False

    def is_locked(self) -> bool:
        return self.LOCK_FILE.exists()

    def is_stale(self) -> bool:
        if not self.is_locked():
            return False

        lock_data = self.get_lock_info()
        if not lock_data:
            return True

        try:
            lock_time = datetime.fromisoformat(lock_data["timestamp"])
        except (KeyError, ValueError):
            return True

        return datetime.now() - lock_time > timedelta(seconds=self.TIMEOUT)

    def get_lock_info(self) -> Optional[Dict]:
        if not self.is_locked():
            return None

        try:
            with open(self.LOCK_FILE, "r", encoding="utf-8") as lock:
                return json.load(lock)
        except (OSError, json.JSONDecodeError):
            return None

    def wait_for_lock(
        self,
        operation_id: str,
        max_wait: int = 60,
        poll_interval: float = 0.5,
    ) -> bool:
        start = time.time()
        while time.time() - start < max_wait:
            if self.acquire_lock(operation_id):
                return True
            time.sleep(poll_interval)
        return False

    def force_release(self) -> None:
        self.release_lock(force=True)

    def _cleanup_handler(self) -> None:
        self.release_lock()

    def _signal_handler(self, signum, frame) -> None:  # pragma: no cover
        self.release_lock()
        raise SystemExit(0)


_lock_manager: Optional[LockManager] = None


def get_lock_manager() -> LockManager:
    global _lock_manager
    if _lock_manager is None:
        _lock_manager = LockManager()
    return _lock_manager
