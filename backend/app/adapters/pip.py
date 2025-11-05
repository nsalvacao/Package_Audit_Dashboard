"""Adapter concreto para o gestor pip."""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

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

    def get_dependency_tree(self, package: Optional[str] = None) -> Dict[str, Any]:
        """Obtém árvore de dependências usando pipdeptree."""
        try:
            # Tenta usar pipdeptree se disponível
            import shutil
            if shutil.which("pipdeptree"):
                args = ["--json"]
                if package:
                    sanitized = self._sanitize_package(package)
                    args.extend(["-p", sanitized])

                result = self.command_executor.run(
                    ["pipdeptree", *args],
                    timeout=self.command_timeout,
                    check=False,
                )

                if result.returncode == 0 and result.stdout:
                    data = json.loads(result.stdout)
                    return {
                        "manager": self.manager_id,
                        "package": package,
                        "tree": data,
                        "supported": True,
                    }

            # Fallback: pip show
            if package:
                sanitized = self._sanitize_package(package)
                result = self.command_executor.run(
                    [self.executable_name, "show", sanitized],
                    timeout=self.command_timeout,
                    check=False,
                )

                if result.returncode == 0:
                    return {
                        "manager": self.manager_id,
                        "package": package,
                        "tree": {"info": result.stdout},
                        "supported": True,
                        "note": "Limited info - install pipdeptree for full tree",
                    }

        except (CommandExecutionError, json.JSONDecodeError) as exc:
            logger.error("Failed to get dependency tree: %s", exc)

        return {
            "manager": self.manager_id,
            "package": package,
            "tree": {},
            "supported": True,
            "error": "Install pipdeptree for dependency tree support",
        }

    def scan_vulnerabilities(self) -> Dict[str, Any]:
        """Escaneia vulnerabilidades usando pip-audit."""
        try:
            # Verifica se pip-audit está disponível
            import shutil
            if not shutil.which("pip-audit"):
                return {
                    "manager": self.manager_id,
                    "vulnerabilities": [],
                    "supported": True,
                    "error": "pip-audit not installed. Run: pip install pip-audit",
                }

            result = self.command_executor.run(
                ["pip-audit", "--format=json"],
                timeout=60,  # Scanning pode demorar
                check=False,
            )

            if result.stdout:
                data = json.loads(result.stdout)
                vulnerabilities = []

                for vuln in data.get("dependencies", []):
                    for advisory in vuln.get("vulns", []):
                        vulnerabilities.append({
                            "id": advisory.get("id"),
                            "severity": advisory.get("fix_versions"),
                            "description": advisory.get("description"),
                            "package": vuln.get("name"),
                            "version": vuln.get("version"),
                        })

                return {
                    "manager": self.manager_id,
                    "vulnerabilities": vulnerabilities,
                    "supported": True,
                }

        except (CommandExecutionError, json.JSONDecodeError) as exc:
            logger.error("Failed to scan vulnerabilities: %s", exc)
            return {
                "manager": self.manager_id,
                "vulnerabilities": [],
                "supported": True,
                "error": str(exc),
            }

    def export_lockfile(self) -> Dict[str, Any]:
        """Exporta requirements.txt."""
        try:
            result = self.command_executor.run(
                [self.executable_name, "freeze"],
                timeout=self.command_timeout,
                check=False,
            )

            if result.returncode == 0 and result.stdout:
                return {
                    "manager": self.manager_id,
                    "lockfile": result.stdout,
                    "supported": True,
                    "format": "requirements.txt",
                }

        except CommandExecutionError as exc:
            logger.error("Failed to export lockfile: %s", exc)

        return {
            "manager": self.manager_id,
            "lockfile": {},
            "supported": True,
            "error": "Failed to export requirements",
        }
