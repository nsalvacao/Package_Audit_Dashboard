"""Testes para SnapshotManager."""
from __future__ import annotations

import pytest

from app.analysis.snapshot_manager import SnapshotManager
from app.core.validation import InvalidPackageNameError, ValidationLayer


@pytest.fixture(autouse=True)
def patch_base_dir(tmp_path, monkeypatch):
    base = tmp_path / ".package-audit"
    monkeypatch.setattr(ValidationLayer, "ALLOWED_BASE_DIR", base)
    return base


def test_create_snapshot_persists_record(monkeypatch):
    manager = SnapshotManager()
    monkeypatch.setattr(manager, "_generate_snapshot_id", lambda: "snap-001")
    monkeypatch.setattr(manager, "_now_iso", lambda: "2025-01-01T00:00:00+00:00")

    summary = manager.create_snapshot(
        {"npm": [{"name": "react", "version": "18.2.0"}]},
        metadata={"reason": "pre-uninstall"},
    )

    assert summary.id == "snap-001"
    assert summary.package_count == 1
    assert summary.managers == ["npm"]

    record = manager.get_snapshot("snap-001")
    assert record["metadata"]["reason"] == "pre-uninstall"
    assert record["managers"]["npm"][0]["name"] == "react"


def test_list_snapshots_returns_sorted(monkeypatch):
    manager = SnapshotManager()
    ids = ["snap-001", "snap-002", "snap-003"]
    timestamps = [
        "2025-01-01T00:00:00+00:00",
        "2025-01-01T00:00:01+00:00",
        "2025-01-01T00:00:02+00:00",
    ]

    for idx in range(3):
        monkeypatch.setattr(manager, "_generate_snapshot_id", lambda i=idx: ids[i])
        monkeypatch.setattr(manager, "_now_iso", lambda i=idx: timestamps[i])
        manager.create_snapshot({"npm": []})

    summaries = manager.list_snapshots()
    assert [s.id for s in summaries] == ["snap-003", "snap-002", "snap-001"]


def test_retention_limit(monkeypatch):
    manager = SnapshotManager()
    manager.RETENTION_LIMIT = 2

    ids = ["snap-a", "snap-b", "snap-c", "snap-d"]
    times = [
        "2025-01-01T00:00:00+00:00",
        "2025-01-01T00:00:01+00:00",
        "2025-01-01T00:00:02+00:00",
        "2025-01-01T00:00:03+00:00",
    ]

    for idx in range(4):
        monkeypatch.setattr(manager, "_generate_snapshot_id", lambda i=idx: ids[i])
        monkeypatch.setattr(manager, "_now_iso", lambda i=idx: times[i])
        manager.create_snapshot({"npm": []})

    summaries = manager.list_snapshots()
    assert len(summaries) == 2
    assert [s.id for s in summaries] == ["snap-d", "snap-c"]
    assert not manager.storage.exists("snap-a.json")


def test_invalid_manager_id(monkeypatch):
    manager = SnapshotManager()
    monkeypatch.setattr(manager, "_generate_snapshot_id", lambda: "snap-err")
    monkeypatch.setattr(manager, "_now_iso", lambda: "2025-01-01T00:00:00+00:00")

    with pytest.raises(InvalidPackageNameError):
        manager.create_snapshot({"BAD MANAGER": []})


def test_restore_snapshot_returns_record(monkeypatch):
    manager = SnapshotManager()
    monkeypatch.setattr(manager, "_generate_snapshot_id", lambda: "snap-restore")
    monkeypatch.setattr(manager, "_now_iso", lambda: "2025-01-01T00:00:00+00:00")
    manager.create_snapshot({"npm": [{"name": "react"}]})

    restored = manager.restore_snapshot("snap-restore")
    assert restored["managers"]["npm"][0]["name"] == "react"
