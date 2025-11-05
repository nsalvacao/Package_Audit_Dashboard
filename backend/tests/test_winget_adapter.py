"""Testes para o WinGetAdapter."""
from __future__ import annotations

import json
import subprocess
from typing import Any, Dict

import pytest

from app.adapters.winget import WinGetAdapter
from app.core.executor import CommandExecutionError
from app.core.validation import InvalidPackageNameError, ValidationLayer


@pytest.fixture(autouse=True)
def patch_base_dir(tmp_path, monkeypatch):
    base = tmp_path / ".package-audit"
    monkeypatch.setattr(ValidationLayer, "ALLOWED_BASE_DIR", base)
    return base


def test_list_packages_parses_output(monkeypatch):
    output = [
        {"Name": "Git", "Id": "Git.Git", "Version": "2.46.0"},
        {"Name": "Node.js LTS", "Id": "OpenJS.NodeJS.LTS", "Version": "20.11.0"},
    ]

    def fake_run(cmd, timeout=None, check=True, cwd=None):
        return subprocess.CompletedProcess(cmd, 0, stdout=json.dumps(output), stderr="")

    monkeypatch.setattr(WinGetAdapter, "command_executor", type("Exec", (), {"run": staticmethod(fake_run)}))
    adapter = WinGetAdapter()
    packages = adapter.list_packages()
    assert {pkg["id"] for pkg in packages} == {"Git.Git", "OpenJS.NodeJS.LTS"}


def test_list_packages_handles_errors(monkeypatch):
    def fake_run(cmd, timeout=None, check=True, cwd=None):
        raise CommandExecutionError("failed")

    monkeypatch.setattr(WinGetAdapter, "command_executor", type("Exec", (), {"run": staticmethod(fake_run)}))
    adapter = WinGetAdapter()
    assert adapter.list_packages() == []


def test_uninstall_builds_command(monkeypatch):
    captured: Dict[str, Any] = {}

    def fake_run(cmd, timeout=None, check=True, cwd=None):
        captured["cmd"] = cmd
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(WinGetAdapter, "command_executor", type("Exec", (), {"run": staticmethod(fake_run)}))
    adapter = WinGetAdapter()
    adapter.uninstall("Git.Git")
    assert captured["cmd"] == [
        "winget",
        "uninstall",
        "--accept-source-agreements",
        "--accept-package-agreements",
        "--id",
        "Git.Git",
    ]


def test_uninstall_with_force(monkeypatch):
    captured: Dict[str, Any] = {}

    def fake_run(cmd, timeout=None, check=True, cwd=None):
        captured["cmd"] = cmd
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(WinGetAdapter, "command_executor", type("Exec", (), {"run": staticmethod(fake_run)}))
    adapter = WinGetAdapter()
    adapter.uninstall("Git.Git", force=True)
    assert captured["cmd"][-1] == "--force"


def test_uninstall_rejects_invalid(monkeypatch):
    adapter = WinGetAdapter()
    with pytest.raises(InvalidPackageNameError):
        adapter.uninstall("Git.Git && remove")


def test_export_manifest(monkeypatch):
    output = [{"Name": "Git", "Id": "Git.Git", "Version": "2.46.0"}]

    def fake_run(cmd, timeout=None, check=True, cwd=None):
        return subprocess.CompletedProcess(cmd, 0, stdout=json.dumps(output), stderr="")

    monkeypatch.setattr(WinGetAdapter, "command_executor", type("Exec", (), {"run": staticmethod(fake_run)}))
    adapter = WinGetAdapter()
    manifest = adapter.export_manifest()
    assert manifest["manager"] == "winget"
    assert manifest["packages"][0]["id"] == "Git.Git"
