"""Testes para o endpoint de uninstall de pacotes."""
from __future__ import annotations

from typing import Any, Dict

import pytest
from fastapi.testclient import TestClient

from app import adapters as adapters_module
from app.adapters import BaseAdapter, registry
from app.analysis.snapshot_manager import SnapshotSummary
from app.core import queue as queue_module
from app.core.validation import ValidationLayer
from app.main import create_app
from app.routers import packages as packages_router


class DummyAdapter(BaseAdapter):
    manager_id = "dummy"
    display_name = "Dummy"
    executable_name = "dummy"

    def list_packages(self):
        return [{"name": "dummy-package", "version": "1.0.0"}]

    def uninstall(self, package: str, force: bool = False) -> Dict[str, Any]:
        return {"success": True, "stdout": "", "stderr": "", "returncode": 0}

    def export_manifest(self):
        return {}


@pytest.fixture(autouse=True)
def patch_allowed_base_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(ValidationLayer, "ALLOWED_BASE_DIR", tmp_path / ".package-audit")


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


@pytest.fixture(autouse=True)
def stub_queue(monkeypatch):
    class FakeQueue:
        async def execute(self, operation_id, operation_type, func, *args, **kwargs):
            return await func(*args, **kwargs)

    monkeypatch.setattr(queue_module, "get_operation_queue", lambda: FakeQueue())
    monkeypatch.setattr(packages_router, "get_operation_queue", lambda: FakeQueue())


@pytest.fixture(autouse=True)
def stub_snapshot_manager(monkeypatch):
    class FakeSnapshotManager:
        def create_snapshot(self, package_map, metadata=None):
            return SnapshotSummary(
                id="snap-001",
                created_at="2025-01-01T00:00:00+00:00",
                managers=list(package_map.keys()),
                package_count=sum(len(v) for v in package_map.values()),
            )

    monkeypatch.setattr(packages_router, "SnapshotManager", FakeSnapshotManager)


def test_uninstall_package_success(monkeypatch, client):
    monkeypatch.setattr(registry, "get_adapter_by_id", lambda mid: DummyAdapter if mid == "dummy" else None)
    monkeypatch.setattr(adapters_module, "get_adapter_by_id", lambda mid: DummyAdapter if mid == "dummy" else None)
    monkeypatch.setattr(packages_router, "get_adapter_by_id", lambda mid: DummyAdapter if mid == "dummy" else None)
    monkeypatch.setattr(DummyAdapter, "detect", classmethod(lambda cls: True))

    response = client.delete("/api/managers/dummy/packages/dummy-package?force=true")
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["success"] is True
    assert body["snapshot_id"] == "snap-001"
    assert body["manager"] == "dummy"
    assert body["package"] == "dummy-package"


def test_uninstall_unknown_manager(monkeypatch, client):
    monkeypatch.setattr(registry, "get_adapter_by_id", lambda mid: None)
    monkeypatch.setattr(adapters_module, "get_adapter_by_id", lambda mid: None)
    monkeypatch.setattr(packages_router, "get_adapter_by_id", lambda mid: None)

    response = client.delete("/api/managers/unknown/packages/pkg")
    assert response.status_code == 404


def test_uninstall_invalid_package(monkeypatch, client):
    monkeypatch.setattr(registry, "get_adapter_by_id", lambda mid: DummyAdapter)
    monkeypatch.setattr(adapters_module, "get_adapter_by_id", lambda mid: DummyAdapter)
    monkeypatch.setattr(packages_router, "get_adapter_by_id", lambda mid: DummyAdapter)
    response = client.delete("/api/managers/dummy/packages/pkg;rm -rf /")
    assert response.status_code == 400


def test_uninstall_requires_detect(monkeypatch, client):
    monkeypatch.setattr(registry, "get_adapter_by_id", lambda mid: DummyAdapter)
    monkeypatch.setattr(adapters_module, "get_adapter_by_id", lambda mid: DummyAdapter)
    monkeypatch.setattr(packages_router, "get_adapter_by_id", lambda mid: DummyAdapter)
    monkeypatch.setattr(DummyAdapter, "detect", classmethod(lambda cls: False))
    response = client.delete("/api/managers/dummy/packages/pkg")
    assert response.status_code == 404
