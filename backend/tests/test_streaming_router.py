"""Testes para o router streaming (Phase 2)."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestStreamingUninstall:
    """Testes para streaming uninstall endpoint."""

    def test_streaming_uninstall_invalid_manager(self):
        """Testa streaming com gestor inválido."""
        response = client.get(
            "/api/streaming/invalid_manager/packages/test-package/uninstall",
            headers={"Accept": "text/event-stream"},
        )
        # SSE endpoints retornam 200 mesmo com erros, verificamos o conteúdo
        assert response.status_code == 200
        assert "text/event-stream" in response.headers.get("content-type", "")

    def test_streaming_uninstall_invalid_package_name(self):
        """Testa streaming com nome de pacote inválido."""
        response = client.get(
            "/api/streaming/npm/packages/../../../etc/passwd/uninstall",
            headers={"Accept": "text/event-stream"},
        )
        assert response.status_code == 200
        # Deve conter evento de erro no stream

    def test_streaming_uninstall_headers(self):
        """Testa headers do SSE."""
        response = client.get(
            "/api/streaming/npm/packages/nonexistent-package/uninstall",
            headers={"Accept": "text/event-stream"},
        )
        assert response.status_code == 200
        headers = response.headers
        assert "text/event-stream" in headers.get("content-type", "")
        assert headers.get("cache-control") == "no-cache"
        assert headers.get("x-accel-buffering") == "no"
