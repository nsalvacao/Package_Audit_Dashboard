"""Testes para o router advanced (Phase 2)."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestDependencyTree:
    """Testes para dependency tree endpoints."""

    def test_get_dependency_tree_invalid_manager(self):
        """Testa dependency tree com gestor inválido."""
        response = client.get("/api/advanced/invalid_manager/dependency-tree")
        assert response.status_code == 404

    def test_get_dependency_tree_npm(self):
        """Testa dependency tree para npm (se disponível)."""
        # Este teste pode falhar se npm não estiver instalado
        response = client.get("/api/advanced/npm/dependency-tree")
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = response.json()
            assert "manager" in data
            assert "tree" in data
            assert "supported" in data

    def test_get_package_dependency_tree(self):
        """Testa dependency tree para um pacote específico."""
        response = client.get("/api/advanced/npm/dependency-tree/express")
        assert response.status_code in [200, 404]


class TestVulnerabilityScanning:
    """Testes para vulnerability scanning."""

    def test_scan_vulnerabilities_invalid_manager(self):
        """Testa scan com gestor inválido."""
        response = client.get("/api/advanced/invalid_manager/vulnerabilities")
        assert response.status_code == 404

    def test_scan_vulnerabilities_npm(self):
        """Testa scan para npm (se disponível)."""
        response = client.get("/api/advanced/npm/vulnerabilities")
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = response.json()
            assert "manager" in data
            assert "vulnerabilities" in data
            assert "supported" in data
            assert isinstance(data["vulnerabilities"], list)

    def test_scan_vulnerabilities_pip(self):
        """Testa scan para pip (se disponível)."""
        response = client.get("/api/advanced/pip/vulnerabilities")
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = response.json()
            assert "manager" in data
            assert "vulnerabilities" in data


class TestLockfileExport:
    """Testes para lockfile export."""

    def test_export_lockfile_invalid_manager(self):
        """Testa export com gestor inválido."""
        response = client.get("/api/advanced/invalid_manager/lockfile")
        assert response.status_code == 404

    def test_export_lockfile_npm(self):
        """Testa export para npm."""
        response = client.get("/api/advanced/npm/lockfile")
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = response.json()
            assert "manager" in data
            assert "lockfile" in data
            assert "supported" in data

    def test_export_lockfile_pip(self):
        """Testa export para pip."""
        response = client.get("/api/advanced/pip/lockfile")
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = response.json()
            assert "manager" in data
            assert "lockfile" in data
            assert "format" in data
            assert data.get("format") == "requirements.txt"


class TestBatchOperations:
    """Testes para batch operations."""

    def test_batch_uninstall_invalid_manager(self):
        """Testa batch uninstall com gestor inválido."""
        response = client.post(
            "/api/advanced/invalid_manager/batch-uninstall",
            json={"packages": ["test-package"], "force": False},
        )
        assert response.status_code == 404

    def test_batch_uninstall_empty_list(self):
        """Testa batch uninstall com lista vazia."""
        response = client.post(
            "/api/advanced/npm/batch-uninstall",
            json={"packages": [], "force": False},
        )
        # Pode retornar 200 ou 404 dependendo se npm está disponível
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = response.json()
            assert data["total"] == 0
            assert data["succeeded"] == []
            assert data["failed"] == []

    def test_batch_uninstall_invalid_package_name(self):
        """Testa batch uninstall com nome de pacote inválido."""
        response = client.post(
            "/api/advanced/npm/batch-uninstall",
            json={"packages": ["../../../etc/passwd"], "force": False},
        )
        assert response.status_code in [400, 404]


class TestRollback:
    """Testes para rollback functionality."""

    def test_rollback_invalid_manager(self):
        """Testa rollback com gestor inválido."""
        response = client.post("/api/advanced/invalid_manager/rollback/test-snapshot-id")
        assert response.status_code == 404

    def test_rollback_invalid_snapshot(self):
        """Testa rollback com snapshot inexistente."""
        response = client.post("/api/advanced/npm/rollback/nonexistent-snapshot")
        assert response.status_code in [404]

    def test_rollback_invalid_snapshot_id(self):
        """Testa rollback com snapshot ID inválido."""
        response = client.post("/api/advanced/npm/rollback/../../../etc/passwd")
        # Deve falhar na validação ou não encontrar
        assert response.status_code in [400, 404]
