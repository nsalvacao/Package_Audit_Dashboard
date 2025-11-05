"""Testes para o endpoint /api/discover."""
from __future__ import annotations

from typing import List, Type

import pytest
from fastapi.testclient import TestClient

from app.adapters import BaseAdapter, NpmAdapter, PipAdapter, WinGetAdapter, BrewAdapter
from app.main import create_app
from app.routers import discover


@pytest.fixture
def client(monkeypatch):
    app = create_app()
    return TestClient(app)


def test_discover_returns_detected_adapters(monkeypatch, client):
    def fake_available() -> List[Type[BaseAdapter]]:
        return [NpmAdapter, PipAdapter]

    monkeypatch.setattr(discover, "_available_adapters", fake_available)
    monkeypatch.setattr(NpmAdapter, "detect", classmethod(lambda cls: True))
    monkeypatch.setattr(PipAdapter, "detect", classmethod(lambda cls: False))
    monkeypatch.setattr(NpmAdapter, "get_version", classmethod(lambda cls: "10.5.0"))
    monkeypatch.setattr(PipAdapter, "get_version", classmethod(lambda cls: "24.0"))

    response = client.post("/api/discover")
    assert response.status_code == 200

    data = response.json()
    assert data == {
        "managers": [
            {"id": "npm", "name": "npm", "version": "10.5.0"},
        ]
    }


def test_discover_returns_unknown_when_version_missing(monkeypatch, client):
    def fake_available() -> List[Type[BaseAdapter]]:
        return [WinGetAdapter, BrewAdapter]

    monkeypatch.setattr(discover, "_available_adapters", fake_available)
    monkeypatch.setattr(WinGetAdapter, "detect", classmethod(lambda cls: True))
    monkeypatch.setattr(WinGetAdapter, "get_version", classmethod(lambda cls: None))
    monkeypatch.setattr(BrewAdapter, "detect", classmethod(lambda cls: False))

    response = client.post("/api/discover")
    assert response.status_code == 200
    data = response.json()
    assert data["managers"][0]["version"] == "unknown"
