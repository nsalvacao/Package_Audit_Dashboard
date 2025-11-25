"""Adapter para o gestor pnpm (global)."""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

from app.adapters.base import BaseAdapter
from app.core.executor import CommandExecutionError

logger = logging.getLogger(__name__)


class PnpmAdapter(BaseAdapter):
    manager_id = "pnpm"
    display_name = "pnpm"
    executable_name = "pnpm"

    LIST_ARGS = ["ls", "-g", "--depth", "1", "--json"]

    def list_packages(self) -> List[Dict[str, Any]]:
        try:
            result = self.command_executor.run(
                [self.executable_name, *self.LIST_ARGS],
                timeout=self.command_timeout,
                check=False,
            )
        except CommandExecutionError as exc:
            logger.error("pnpm list falhou: %s", exc)
            return []

        output = result.stdout or result.stderr
        if not output:
            return []

        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            logger.warning("pnpm list retornou JSON inválido.")
            return []

        packages: List[Dict[str, Any]] = []
        for entry in data:
            # entries have name + version
            name = entry.get("name") or entry.get("package", {}).get("name")
            version = entry.get("version") or entry.get("package", {}).get("version")
            if name:
                packages.append(
                    {
                        "name": name,
                        "version": version,
                        "status": "unknown",
                        "manager": self.manager_id,
                    }
                )
        return packages

    def uninstall(self, package: str, force: bool = False) -> Dict[str, Any]:
        sanitized = self._sanitize_package(package)
        args = ["remove", "-g", sanitized]
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

    def get_dependency_tree(self, package: str | None = None) -> Dict[str, Any]:
        # Use pnpm ls to build a simple tree
        try:
            args = ["ls", "-g", "--json"]
            if package:
                args.extend(["-r", package])

            result = self.command_executor.run(
                [self.executable_name, *args], timeout=self.command_timeout, check=False
            )
            if result.returncode == 0 and result.stdout:
                return {
                    "manager": self.manager_id,
                    "package": package,
                    "tree": json.loads(result.stdout),
                    "supported": True,
                }
        except (CommandExecutionError, json.JSONDecodeError) as exc:
            logger.error("pnpm dependency tree falhou: %s", exc)

        return {
            "manager": self.manager_id,
            "package": package,
            "tree": {},
            "supported": True,
            "error": "Failed to build dependency tree",
        }

    def export_lockfile(self) -> Dict[str, Any]:
        try:
            # There is no global lockfile; export list as pseudo-lock
            manifest = self.export_manifest()
            return {
                "manager": self.manager_id,
                "lockfile": manifest,
                "supported": True,
                "format": "pnpm-list.json",
            }
        except Exception as exc:
            return {
                "manager": self.manager_id,
                "lockfile": {},
                "supported": True,
                "error": str(exc),
            }
