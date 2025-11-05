"""Armazenamento seguro em JSON dentro do diretório controlado."""
from __future__ import annotations

import json
import logging
import os
import tempfile
from pathlib import Path
from typing import Any

from app.core.validation import PathTraversalError, ValidationLayer


logger = logging.getLogger(__name__)


class JSONStorage:
    """Gestor simples para leitura/escrita de ficheiros JSON."""

    DEFAULT_SUBDIR = "storage"

    def __init__(self, base_dir: Path | None = None) -> None:
        allowed_base = ValidationLayer.ALLOWED_BASE_DIR
        self.base_dir = base_dir or allowed_base / self.DEFAULT_SUBDIR
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _resolve_path(self, relative_path: str) -> Path:
        target = Path(relative_path)
        if target.is_absolute():
            raise PathTraversalError("Absolute paths are not allowed.")

        full_path = (self.base_dir / target).resolve()

        try:
            full_path.relative_to(self.base_dir)
        except ValueError as exc:
            raise PathTraversalError(
                f"Path escapes storage directory: {relative_path}"
            ) from exc

        return full_path

    def exists(self, relative_path: str) -> bool:
        return self._resolve_path(relative_path).exists()

    def read(self, relative_path: str) -> Any:
        path = self._resolve_path(relative_path)
        logger.debug("Reading JSON from %s", path)
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)

    def write(self, relative_path: str, data: Any) -> Path:
        path = self._resolve_path(relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        logger.debug("Writing JSON to %s", path)
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            delete=False,
            dir=str(path.parent),
            suffix=".tmp",
        ) as tmp:
            json.dump(data, tmp, indent=2)
            tmp.flush()
            os.fsync(tmp.fileno())
            temp_name = tmp.name

        os.replace(temp_name, path)
        return path

    def delete(self, relative_path: str) -> bool:
        path = self._resolve_path(relative_path)
        if not path.exists():
            return False
        logger.debug("Deleting JSON file %s", path)
        path.unlink()
        return True
