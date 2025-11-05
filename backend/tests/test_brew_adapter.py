"""Testes para o BrewAdapter."""
from __future__ import annotations

import json
import subprocess
from typing import Any, Dict

import pytest

from app.adapters.brew import BrewAdapter
from app.core.executor import CommandExecutionError
from app.core.validation import InvalidPackageNameError, ValidationLayer


@pytest.fixture(autouse=True)
def patch_base_dir(tmp_path, monkeypatch):
    base = tmp_path / ".package-audit"
    monkeypatch.setattr(ValidationLayer, "ALLOWED_BASE_DIR", base)
    return base


def test_list_packages_parses_formulae(monkeypatch):
    output = {
        "formulae": [
            {"name": "python", "installed": [{"version": "3.12.4"}]},
            {"name": "node", "installed": [{"version": "20.11.0"}]},
        ]
    }

    def fake_run(cmd, timeout=None, check=True, cwd=None):
        return subprocess.CompletedProcess(cmd, 0, stdout=json.dumps(output), stderr="")

    monkeypatch.setattr(BrewAdapter, "command_executor", type("Exec", (), {"run": staticmethod(fake_run)}))
    adapter = BrewAdapter()
    packages = adapter.list_packages()
    assert {pkg["name"] for pkg in packages} == {"python", "node"}


def test_list_packages_handles_errors(monkeypatch):
    def fake_run(cmd, timeout=None, check=True, cwd=None):
        raise CommandExecutionError("failed")

    monkeypatch.setattr(BrewAdapter, "command_executor", type("Exec", (), {"run": staticmethod(fake_run)}))
    adapter = BrewAdapter()
    assert adapter.list_packages() == []


def test_uninstall_builds_command(monkeypatch):
    captured: Dict[str, Any] = {}

    def fake_run(cmd, timeout=None, check=True, cwd=None):
        captured["cmd"] = cmd
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(BrewAdapter, "command_executor", type("Exec", (), {"run": staticmethod(fake_run)}))
    adapter = BrewAdapter()
    adapter.uninstall("python")
    assert captured["cmd"] == ["brew", "uninstall", "python"]


def test_uninstall_with_force(monkeypatch):
    captured: Dict[str, Any] = {}

    def fake_run(cmd, timeout=None, check=True, cwd=None):
        captured["cmd"] = cmd
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(BrewAdapter, "command_executor", type("Exec", (), {"run": staticmethod(fake_run)}))
    adapter = BrewAdapter()
    adapter.uninstall("python", force=True)
    assert captured["cmd"] == ["brew", "uninstall", "--force", "python"]


def test_uninstall_rejects_invalid(monkeypatch):
    adapter = BrewAdapter()
    with pytest.raises(InvalidPackageNameError):
        adapter.uninstall("python; rm -rf /")


def test_export_manifest(monkeypatch):
    output = {"formulae": [{"name": "python", "installed": [{"version": "3.12.4"}]}]}

    def fake_run(cmd, timeout=None, check=True, cwd=None):
        return subprocess.CompletedProcess(cmd, 0, stdout=json.dumps(output), stderr="")

    monkeypatch.setattr(BrewAdapter, "command_executor", type("Exec", (), {"run": staticmethod(fake_run)}))
    adapter = BrewAdapter()
    manifest = adapter.export_manifest()
    assert manifest["manager"] == "brew"
    assert manifest["packages"][0]["name"] == "python"
