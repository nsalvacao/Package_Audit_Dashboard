"""Testes unitários para BaseAdapter."""
from __future__ import annotations

import subprocess
from typing import Any, Dict, List

import pytest

from app.adapters.base import BaseAdapter
from app.core.executor import CommandExecutionError
from app.core.validation import InvalidPackageNameError, ValidationLayer


class DummyAdapter(BaseAdapter):
    manager_id = "dummy"
    display_name = "Dummy Manager"
    executable_name = "dummy"

    def list_packages(self) -> List[Dict[str, Any]]:
        return []

    def uninstall(self, package: str, force: bool = False) -> Dict[str, Any]:
        return {"package": package, "force": force}

    def export_manifest(self) -> Dict[str, Any]:
        return {"packages": []}


@pytest.fixture(autouse=True)
def patch_allowed_base_dir(tmp_path, monkeypatch):
    base = tmp_path / ".package-audit"
    monkeypatch.setattr(ValidationLayer, "ALLOWED_BASE_DIR", base)
    return base


def test_detect_returns_true_when_executable_found(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/dummy")
    assert DummyAdapter.detect() is True


def test_detect_returns_false_when_missing(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda _: None)
    assert DummyAdapter.detect() is False


def test_get_version_returns_output(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/dummy")

    def fake_run(cmd, timeout=None, check=True, cwd=None):
        return subprocess.CompletedProcess(cmd, 0, stdout="v1.2.3\n", stderr="")

    monkeypatch.setattr(DummyAdapter, "command_executor", type("Exec", (), {"run": staticmethod(fake_run)}))
    assert DummyAdapter.get_version() == "v1.2.3"


def test_get_version_handles_errors(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/dummy")

    def fake_run(cmd, timeout=None, check=True, cwd=None):
        raise CommandExecutionError("boom")

    monkeypatch.setattr(DummyAdapter, "command_executor", type("Exec", (), {"run": staticmethod(fake_run)}))
    assert DummyAdapter.get_version() is None


def test_build_package_command_sanitizes(monkeypatch):
    adapter = DummyAdapter()
    cmd = adapter.build_package_command(["uninstall"], ["valid-package"])
    assert cmd == ["dummy", "uninstall", "valid-package"]

    with pytest.raises(InvalidPackageNameError):
        adapter.build_package_command(["uninstall"], ["rm -rf /"])


def test_run_command_uses_executor(monkeypatch):
    captured = {}

    def fake_run(cmd, timeout=None, check=True, cwd=None):
        captured["cmd"] = cmd
        captured["timeout"] = timeout
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(DummyAdapter, "command_executor", type("Exec", (), {"run": staticmethod(fake_run)}))
    adapter = DummyAdapter()
    adapter.run_command(["list"])
    assert captured["cmd"] == ["dummy", "list"]


def test_cache_operations(tmp_path):
    adapter = DummyAdapter()
    data = {"value": 42}
    adapter.cache_write("test.json", data)
    assert adapter.cache_exists("test.json")
    assert adapter.cache_read("test.json") == data
    assert adapter.cache_delete("test.json") is True
    assert adapter.cache_exists("test.json") is False
