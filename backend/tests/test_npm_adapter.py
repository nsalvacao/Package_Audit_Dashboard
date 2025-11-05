"""Testes para o NpmAdapter."""
from __future__ import annotations

import json
import subprocess
from typing import Any, Dict

import pytest

from app.adapters.npm import NpmAdapter
from app.core.executor import CommandExecutionError
from app.core.validation import InvalidPackageNameError, ValidationLayer


@pytest.fixture(autouse=True)
def patch_base_dir(tmp_path, monkeypatch):
    base = tmp_path / ".package-audit"
    monkeypatch.setattr(ValidationLayer, "ALLOWED_BASE_DIR", base)
    return base


def test_list_packages_parses_dependencies(monkeypatch):
    output = {
        "dependencies": {
            "react": {"version": "18.2.0"},
            "eslint": {"version": "8.0.0"},
        }
    }

    def fake_run(cmd, timeout=None, check=True, cwd=None):
        return subprocess.CompletedProcess(cmd, 0, stdout=json.dumps(output), stderr="")

    monkeypatch.setattr(NpmAdapter, "command_executor", type("Exec", (), {"run": staticmethod(fake_run)}))
    adapter = NpmAdapter()
    packages = adapter.list_packages()
    assert {pkg["name"] for pkg in packages} == {"react", "eslint"}


def test_list_packages_handles_errors(monkeypatch):
    def fake_run(cmd, timeout=None, check=True, cwd=None):
        raise CommandExecutionError("failed")

    monkeypatch.setattr(NpmAdapter, "command_executor", type("Exec", (), {"run": staticmethod(fake_run)}))
    adapter = NpmAdapter()
    assert adapter.list_packages() == []


def test_uninstall_constructs_command(monkeypatch):
    captured: Dict[str, Any] = {}

    def fake_run(cmd, timeout=None, check=True, cwd=None):
        captured["cmd"] = cmd
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(NpmAdapter, "command_executor", type("Exec", (), {"run": staticmethod(fake_run)}))
    adapter = NpmAdapter()
    result = adapter.uninstall("react")
    assert result["success"] is True
    assert captured["cmd"] == ["npm", "uninstall", "-g", "react"]


def test_uninstall_with_force(monkeypatch):
    captured: Dict[str, Any] = {}

    def fake_run(cmd, timeout=None, check=True, cwd=None):
        captured["cmd"] = cmd
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(NpmAdapter, "command_executor", type("Exec", (), {"run": staticmethod(fake_run)}))
    adapter = NpmAdapter()
    adapter.uninstall("react", force=True)
    assert captured["cmd"] == ["npm", "uninstall", "-g", "--force", "react"]


def test_uninstall_rejects_invalid_package(monkeypatch):
    adapter = NpmAdapter()
    with pytest.raises(InvalidPackageNameError):
        adapter.uninstall("react && rm -rf /")


def test_export_manifest(monkeypatch):
    packages = [{"name": "react", "version": "18.2.0"}]

    def fake_run(cmd, timeout=None, check=True, cwd=None):
        return subprocess.CompletedProcess(cmd, 0, stdout=json.dumps({"dependencies": {"react": {"version": "18.2.0"}}}), stderr="")

    monkeypatch.setattr(NpmAdapter, "command_executor", type("Exec", (), {"run": staticmethod(fake_run)}))
    adapter = NpmAdapter()
    manifest = adapter.export_manifest()
    assert manifest["manager"] == "npm"
    assert manifest["packages"][0]["name"] == "react"
