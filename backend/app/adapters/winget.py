"""Adapter concreto para o gestor WinGet (Windows)."""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

from app.adapters.base import BaseAdapter
from app.core.executor import CommandExecutionError

logger = logging.getLogger(__name__)


class WinGetAdapter(BaseAdapter):
    """Opera sobre o gestor WinGet."""

    manager_id = "winget"
    display_name = "WinGet"
    executable_name = "winget"

    LIST_ARGS = [
        "list",
        "--accept-source-agreements",
        "--accept-package-agreements",
        "--output",
        "json",
    ]
    UNINSTALL_ARGS = [
        "uninstall",
        "--accept-source-agreements",
        "--accept-package-agreements",
    ]

    def list_packages(self) -> List[Dict[str, Any]]:
        try:
            result = self.command_executor.run(
                [self.executable_name, *self.LIST_ARGS],
                timeout=self.command_timeout,
                check=False,
            )
        except CommandExecutionError as exc:
            logger.error("winget list falhou: %s", exc)
            return []

        output = result.stdout or result.stderr
        if not output:
            return []

        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            logger.warning("winget list retornou JSON inválido.")
            return []

        packages: List[Dict[str, Any]] = []
        for entry in data:
            packages.append(
                {
                    "name": entry.get("Name"),
                    "id": entry.get("Id"),
                    "version": entry.get("Version"),
                    "status": "unknown",
                    "manager": self.manager_id,
                }
            )
        return packages

    def uninstall(self, package: str, force: bool = False) -> Dict[str, Any]:
        sanitized = self._sanitize_package(package)
        args = list(self.UNINSTALL_ARGS)
        args.extend(["--id", sanitized])
        if force:
            args.append("--force")

        command = [self.executable_name, *args]
        result = self.command_executor.run(
            command,
            timeout=self.command_timeout,
            check=False,
        )

        success = result.returncode == 0
        if not success:
            logger.error(
                "winget uninstall falhou para %s (code %s)",
                sanitized,
                result.returncode,
            )

        return {
            "success": success,
            "package": sanitized,
            "force": force,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }

    def export_manifest(self) -> Dict[str, Any]:
        packages = self.list_packages()
        return {
            "manager": self.manager_id,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "packages": packages,
        }

    def get_dependency_tree(self, package: str | None = None) -> Dict[str, Any]:
        """Winget não expõe dependências; devolve árvore plana das instalações."""
        packages = self.list_packages()
        return {
            "manager": self.manager_id,
            "package": package,
            "tree": {"packages": packages},
            "supported": True,
            "note": "Winget não fornece árvore de dependências; lista plana retornada.",
        }

    def export_lockfile(self) -> Dict[str, Any]:
        """Exporta manifest via winget export."""
        try:
            result = self.command_executor.run(
                [
                    self.executable_name,
                    "export",
                    "--output",
                    "-",
                    "--accept-source-agreements",
                    "--accept-package-agreements",
                    "--disable-interactivity",
                    "--json",
                ],
                timeout=self.command_timeout,
                check=False,
            )
            if result.returncode == 0 and result.stdout:
                try:
                    data = json.loads(result.stdout)
                except json.JSONDecodeError:
                    data = {"raw": result.stdout}
                return {
                    "manager": self.manager_id,
                    "lockfile": data,
                    "supported": True,
                    "format": "winget-export.json",
                }
        except CommandExecutionError as exc:
            logger.error("Failed to export winget lockfile: %s", exc)

        return {
            "manager": self.manager_id,
            "lockfile": {},
            "supported": True,
            "error": "Failed to export winget lockfile",
        }
