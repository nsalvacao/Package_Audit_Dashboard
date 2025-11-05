"""Testes para JSONStorage."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.core.validation import PathTraversalError, ValidationLayer
from app.storage.json_storage import JSONStorage


@pytest.fixture
def storage(tmp_path, monkeypatch):
    base = tmp_path / ".package-audit"
    monkeypatch.setattr(ValidationLayer, "ALLOWED_BASE_DIR", base)
    store = JSONStorage(base_dir=base / "storage")
    return store


def test_write_and_read_json(storage):
    data = {"name": "snapshot", "packages": ["a", "b"]}
    storage.write("snapshots/test.json", data)
    loaded = storage.read("snapshots/test.json")
    assert loaded == data


def test_exists(storage):
    storage.write("managers/npm.json", {"count": 3})
    assert storage.exists("managers/npm.json")
    assert not storage.exists("managers/pip.json")


def test_delete(storage):
    storage.write("snapshots/old.json", {"ok": True})
    assert storage.delete("snapshots/old.json")
    assert not storage.exists("snapshots/old.json")
    assert not storage.delete("snapshots/old.json")


def test_read_missing_file(storage):
    with pytest.raises(FileNotFoundError):
        storage.read("missing.json")


def test_reject_absolute_path(storage):
    with pytest.raises(PathTraversalError):
        storage.write("/etc/passwd", {})


def test_reject_traversal(storage):
    with pytest.raises(PathTraversalError):
        storage.read("../outside.json")


def test_atomic_write(storage, tmp_path):
    rel_path = "atomic/test.json"
    data = {"value": 1}
    path = storage.write(rel_path, data)
    with open(path, "r", encoding="utf-8") as handle:
        content = json.load(handle)
    assert content == data
