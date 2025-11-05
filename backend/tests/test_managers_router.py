"""Testes para o endpoint /api/managers."""
from __future__ import annotations

from typing import List, Type

import pytest
from fastapi.testclient import TestClient

from app import adapters as adapters_module
from app.adapters import BaseAdapter, NpmAdapter, PipAdapter
from app.adapters import registry
from app.main import create_app
from app.routers import managers as managers_router


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_list_managers_returns_detected(monkeypatch, client):
    def fake_registered() -> List[Type[BaseAdapter]]:
        return [NpmAdapter, PipAdapter]

    monkeypatch.setattr(registry, "get_registered_adapters", fake_registered)
    monkeypatch.setattr(adapters_module, "get_registered_adapters", fake_registered)
    monkeypatch.setattr(managers_router, "get_registered_adapters", fake_registered)
    monkeypatch.setattr(NpmAdapter, "detect", classmethod(lambda cls: True))
    monkeypatch.setattr(NpmAdapter, "get_version", classmethod(lambda cls: "10.5.0"))
    monkeypatch.setattr(PipAdapter, "detect", classmethod(lambda cls: True))
    monkeypatch.setattr(PipAdapter, "get_version", classmethod(lambda cls: None))

    response = client.get("/api/managers")
    assert response.status_code == 200
    data = response.json()
    assert len(data["managers"]) == 2
    npm_entry = next(item for item in data["managers"] if item["id"] == "npm")
    assert npm_entry["version"] == "10.5.0"
    pip_entry = next(item for item in data["managers"] if item["id"] == "pip")
    assert pip_entry["version"] == "unknown"
    assert "uninstall" in npm_entry["capabilities"]


def test_list_managers_returns_empty_when_none(monkeypatch, client):
    monkeypatch.setattr(registry, "get_registered_adapters", lambda: [NpmAdapter])
    monkeypatch.setattr(adapters_module, "get_registered_adapters", lambda: [NpmAdapter])
    monkeypatch.setattr(managers_router, "get_registered_adapters", lambda: [NpmAdapter])
    monkeypatch.setattr(NpmAdapter, "detect", classmethod(lambda cls: False))

    response = client.get("/api/managers")
    assert response.status_code == 200
    assert response.json() == {"managers": []}
