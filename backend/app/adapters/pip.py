"""Adapter concreto para o gestor pip."""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

from app.adapters.base import BaseAdapter
from app.core.executor import CommandExecutionError

logger = logging.getLogger(__name__)


class PipAdapter(BaseAdapter):
    """Opera sobre o gestor pip global."""

    manager_id = "pip"
    display_name = "pip"
    executable_name = "pip"

    LIST_ARGS = ["list", "--format=json"]
    UNINSTALL_ARGS = ["uninstall"]

    def list_packages(self) -> List[Dict[str, Any]]:
        try:
            result = self.command_executor.run(
                [self.executable_name, *self.LIST_ARGS],
                timeout=self.command_timeout,
                check=False,
            )
        except CommandExecutionError as exc:
            logger.error("pip list falhou: %s", exc)
            return []

        output = result.stdout or result.stderr
        if not output:
            return []

        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            logger.warning("pip list retornou JSON inválido.")
            return []

        packages: List[Dict[str, Any]] = []
        for entry in data:
            packages.append(
                {
                    "name": entry.get("name"),
                    "version": entry.get("version"),
                    "status": "unknown",
                    "manager": self.manager_id,
                }
            )
        return packages

    def uninstall(self, package: str, force: bool = False) -> Dict[str, Any]:
        sanitized = self._sanitize_package(package)
        args = list(self.UNINSTALL_ARGS)
        args.append("-y")
        command = self.build_package_command(args, [sanitized])

        result = self.command_executor.run(
            command,
            timeout=self.command_timeout,
            check=False,
        )

        success = result.returncode == 0
        if not success:
            logger.error(
                "pip uninstall falhou para %s (code %s)",
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
