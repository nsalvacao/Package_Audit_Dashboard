"""Gestor de snapshots em JSON para estados dos gestores de pacotes."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

from app.core.validation import ValidationLayer
from app.storage.json_storage import JSONStorage


@dataclass
class SnapshotSummary:
    """Resumo de um snapshot armazenado."""

    id: str
    created_at: str
    managers: List[str]
    package_count: int


class SnapshotManager:
    """Criação, listagem e recuperação de snapshots."""

    RETENTION_LIMIT = 10

    def __init__(self, storage: Optional[JSONStorage] = None) -> None:
        base_dir = ValidationLayer.ALLOWED_BASE_DIR / "snapshots"
        self.storage = storage or JSONStorage(base_dir=base_dir)

    def create_snapshot(
        self,
        package_map: Dict[str, List[Dict[str, Any]]],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> SnapshotSummary:
        """Cria snapshot com o mapa de pacotes por gestor."""
        if not isinstance(package_map, dict):
            raise TypeError("package_map deve ser um dicionário {manager: packages}.")

        sanitized: Dict[str, List[Dict[str, Any]]] = {}
        for manager_id, packages in package_map.items():
            clean_id = ValidationLayer.sanitize_manager_id(manager_id)
            sanitized[clean_id] = list(packages or [])

        snapshot_id = self._generate_snapshot_id()
        created_at = self._now_iso()
        package_count = sum(len(items) for items in sanitized.values())
        record = {
            "id": snapshot_id,
            "created_at": created_at,
            "package_count": package_count,
            "managers": sanitized,
            "metadata": metadata or {},
        }

        self.storage.write(f"{snapshot_id}.json", record)
        self._enforce_retention()
        return self._summary_from_record(record)

    def list_snapshots(self) -> List[SnapshotSummary]:
        """Lista snapshots existentes por ordem decrescente de criação."""
        summaries: List[SnapshotSummary] = []
        for file in sorted(self.storage.base_dir.glob("*.json")):
            record = self.storage.read(file.name)
            summaries.append(self._summary_from_record(record))

        summaries.sort(
            key=lambda summary: datetime.fromisoformat(summary.created_at),
            reverse=True,
        )
        return summaries

    def get_snapshot(self, snapshot_id: str) -> Dict[str, Any]:
        """Obtém o conteúdo completo de um snapshot."""
        return self.storage.read(f"{snapshot_id}.json")

    def restore_snapshot(self, snapshot_id: str) -> Dict[str, Any]:
        """Placeholder para restore – retorna o snapshot para uso externo."""
        return self.get_snapshot(snapshot_id)

    def delete_snapshot(self, snapshot_id: str) -> bool:
        """Remove snapshot específico."""
        return self.storage.delete(f"{snapshot_id}.json")

    # --- Helpers ----------------------------------------------------------------------

    def _generate_snapshot_id(self) -> str:
        """Gera identificador único."""
        while True:
            candidate = f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}-{uuid4().hex[:6]}"
            if not self.storage.exists(f"{candidate}.json"):
                return candidate

    @staticmethod
    def _summary_from_record(record: Dict[str, Any]) -> SnapshotSummary:
        return SnapshotSummary(
            id=record["id"],
            created_at=record["created_at"],
            managers=sorted(record.get("managers", {}).keys()),
            package_count=record.get("package_count", 0),
        )

    def _enforce_retention(self) -> None:
        summaries = self.list_snapshots()
        if len(summaries) <= self.RETENTION_LIMIT:
            return

        for summary in summaries[self.RETENTION_LIMIT :]:
            self.storage.delete(f"{summary.id}.json")

    @staticmethod
    def _now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()
