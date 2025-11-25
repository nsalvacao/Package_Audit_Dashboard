"""Adapter para o gestor pipx."""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

from app.adapters.base import BaseAdapter
from app.core.executor import CommandExecutionError

logger = logging.getLogger(__name__)


class PipxAdapter(BaseAdapter):
    manager_id = "pipx"
    display_name = "pipx"
    executable_name = "pipx"

    def list_packages(self) -> List[Dict[str, Any]]:
        try:
            result = self.command_executor.run(
                [self.executable_name, "list", "--json"],
                timeout=self.command_timeout,
                check=False,
            )
        except CommandExecutionError as exc:
            logger.error("pipx list falhou: %s", exc)
            return []

        output = result.stdout or result.stderr
        if not output:
            return []

        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            logger.warning("pipx list retornou JSON inválido.")
            return []

        packages: List[Dict[str, Any]] = []
        for pkg in data.get("venvs", {}).values():
            meta = pkg.get("metadata", {})
            package_name = meta.get("main_package", {}).get("package")
            version = meta.get("main_package", {}).get("package_version")
            if package_name:
                packages.append(
                    {
                        "name": package_name,
                        "version": version,
                        "status": "unknown",
                        "manager": self.manager_id,
                    }
                )
        return packages

    def uninstall(self, package: str, force: bool = False) -> Dict[str, Any]:
        sanitized = self._sanitize_package(package)
        args = ["uninstall", sanitized]
        if force:
            args.append("--force")

        result = self.command_executor.run(
            [self.executable_name, *args],
            timeout=self.command_timeout,
            check=False,
        )

        success = result.returncode == 0
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

    def export_lockfile(self) -> Dict[str, Any]:
        manifest = self.export_manifest()
        return {
            "manager": self.manager_id,
            "lockfile": manifest,
            "supported": True,
            "format": "pipx-list.json",
        }

