"""Adapter concreto para o gestor npm."""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.adapters.base import BaseAdapter
from app.core.executor import CommandExecutionError
from app.core.validation import InvalidPackageNameError, ValidationLayer

logger = logging.getLogger(__name__)


class NpmAdapter(BaseAdapter):
    """Opera sobre o gestor npm (global)."""

    manager_id = "npm"
    display_name = "npm"
    executable_name = "npm"

    LIST_ARGS = ["list", "-g", "--depth=0", "--json"]
    UNINSTALL_ARGS = ["uninstall", "-g"]

    def list_packages(self) -> List[Dict[str, Any]]:
        try:
            result = self.command_executor.run(
                [self.executable_name, *self.LIST_ARGS],
                timeout=self.command_timeout,
                check=False,
            )
        except CommandExecutionError as exc:
            logger.error("npm list failed: %s", exc)
            return []

        output = result.stdout or result.stderr
        if not output:
            return []

        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            logger.warning("npm list returned invalid JSON.")
            return []

        dependencies = data.get("dependencies", {})
        packages: List[Dict[str, Any]] = []
        for name, meta in dependencies.items():
            version = meta.get("version")
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
        args = list(self.UNINSTALL_ARGS)
        if force:
            args.append("--force")
        command = self.build_package_command(args, [sanitized])

        result = self.command_executor.run(
            command,
            timeout=self.command_timeout,
            check=False,
        )

        success = result.returncode == 0
        if not success:
            logger.error(
                "npm uninstall failed for %s (code %s)",
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
