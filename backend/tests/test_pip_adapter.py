"""Testes para o PipAdapter."""
from __future__ import annotations

import json
import subprocess
from typing import Any, Dict

import pytest

from app.adapters.pip import PipAdapter
from app.core.executor import CommandExecutionError
from app.core.validation import InvalidPackageNameError, ValidationLayer


@pytest.fixture(autouse=True)
def patch_base_dir(tmp_path, monkeypatch):
    base = tmp_path / ".package-audit"
    monkeypatch.setattr(ValidationLayer, "ALLOWED_BASE_DIR", base)
    return base


def test_list_packages_parses_output(monkeypatch):
    output = [
        {"name": "requests", "version": "2.31.0"},
        {"name": "pytest", "version": "8.4.2"},
    ]

    def fake_run(cmd, timeout=None, check=True, cwd=None):
        return subprocess.CompletedProcess(cmd, 0, stdout=json.dumps(output), stderr="")

    monkeypatch.setattr(PipAdapter, "command_executor", type("Exec", (), {"run": staticmethod(fake_run)}))
    adapter = PipAdapter()
    packages = adapter.list_packages()
    assert {pkg["name"] for pkg in packages} == {"requests", "pytest"}


def test_list_packages_returns_empty_on_error(monkeypatch):
    def fake_run(cmd, timeout=None, check=True, cwd=None):
        raise CommandExecutionError("failed")

    monkeypatch.setattr(PipAdapter, "command_executor", type("Exec", (), {"run": staticmethod(fake_run)}))
    adapter = PipAdapter()
    assert adapter.list_packages() == []


def test_uninstall_builds_command(monkeypatch):
    captured: Dict[str, Any] = {}

    def fake_run(cmd, timeout=None, check=True, cwd=None):
        captured["cmd"] = cmd
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(PipAdapter, "command_executor", type("Exec", (), {"run": staticmethod(fake_run)}))
    adapter = PipAdapter()
    result = adapter.uninstall("requests")
    assert result["success"] is True
    assert captured["cmd"] == ["pip", "uninstall", "-y", "requests"]


def test_uninstall_rejects_invalid_package():
    adapter = PipAdapter()
    with pytest.raises(InvalidPackageNameError):
        adapter.uninstall("requests; rm -rf /")


def test_export_manifest(monkeypatch):
    output = [{"name": "numpy", "version": "1.26.0"}]

    def fake_run(cmd, timeout=None, check=True, cwd=None):
        return subprocess.CompletedProcess(cmd, 0, stdout=json.dumps(output), stderr="")

    monkeypatch.setattr(PipAdapter, "command_executor", type("Exec", (), {"run": staticmethod(fake_run)}))
    adapter = PipAdapter()
    manifest = adapter.export_manifest()
    assert manifest["manager"] == "pip"
    assert manifest["packages"][0]["name"] == "numpy"
