"""Validation layer para inputs e comandos críticos."""
from __future__ import annotations

import re
from pathlib import Path
from typing import List


class InvalidPackageNameError(ValueError):
    """Uso de nome de pacote inválido."""


class PathTraversalError(ValueError):
    """Tentativa de aceder a caminho fora da área permitida."""


class ValidationLayer:
    """Concentra validações de nomes, comandos e caminhos."""

    PACKAGE_NAME_REGEX = re.compile(r"^[a-zA-Z0-9@/_.-]+$")
    MAX_PACKAGE_NAME_LENGTH = 214
    ALLOWED_BASE_DIR = Path.home() / ".package-audit"

    @staticmethod
    def sanitize_package_name(name: str) -> str:
        if not name:
            raise InvalidPackageNameError("Package name cannot be empty")

        if len(name) > ValidationLayer.MAX_PACKAGE_NAME_LENGTH:
            raise InvalidPackageNameError(
                f"Package name too long (max {ValidationLayer.MAX_PACKAGE_NAME_LENGTH}): {name}"
            )

        if not ValidationLayer.PACKAGE_NAME_REGEX.match(name):
            raise InvalidPackageNameError(
                f"Package name contains invalid characters: {name}"
            )

        if ".." in name:
            raise InvalidPackageNameError(
                f"Package name contains forbidden sequence '..': {name}"
            )

        return name

    @staticmethod
    def build_safe_command(base_cmd: List[str], args: List[str]) -> List[str]:
        if not isinstance(base_cmd, list):
            raise TypeError("base_cmd must be a list")

        if not isinstance(args, list):
            raise TypeError("args must be a list")

        sanitized_args = [
            ValidationLayer.sanitize_package_name(arg) for arg in args
        ]
        return base_cmd + sanitized_args

    @staticmethod
    def validate_path(path: str) -> Path:
        base_dir = ValidationLayer.ALLOWED_BASE_DIR
        base_dir.mkdir(parents=True, exist_ok=True)

        full_path = Path(path)
        if not full_path.is_absolute():
            full_path = base_dir / path

        real_path = full_path.resolve()

        try:
            real_path.relative_to(base_dir)
        except ValueError as exc:
            raise PathTraversalError(
                f"Path outside allowed directory: {path}"
            ) from exc

        return real_path

    @staticmethod
    def sanitize_manager_id(manager_id: str) -> str:
        if not re.match(r"^[a-z][a-z0-9_-]*$", manager_id):
            raise InvalidPackageNameError(f"Invalid manager ID: {manager_id}")

        if len(manager_id) > 50:
            raise InvalidPackageNameError(
                f"Manager ID too long: {manager_id}"
            )

        return manager_id
