"""BaseAdapter que normaliza operações entre gestores de pacotes."""
from __future__ import annotations

import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

from app.core.executor import (
    CommandExecutionError,
    CommandExecutor,
    CommandTimeoutError,
)
from app.core.validation import InvalidPackageNameError, ValidationLayer
from app.storage.json_storage import JSONStorage


class BaseAdapter(ABC):
    """Classe base para gestores de pacotes suportados pelo dashboard."""

    manager_id: str = ""
    display_name: str = ""
    executable_name: str = ""
    version_args: List[str] = ["--version"]
    command_timeout: int = CommandExecutor.DEFAULT_TIMEOUT
    command_executor: Type[CommandExecutor] = CommandExecutor

    def __init__(
        self,
        storage: Optional[JSONStorage] = None,
    ) -> None:
        if not self.manager_id or not self.executable_name:
            raise ValueError("Subclasses devem definir manager_id e executable_name.")

        self.storage = storage or JSONStorage(
            base_dir=ValidationLayer.ALLOWED_BASE_DIR / "storage"
        )

    # --- Interface pública obrigatória -------------------------------------------------

    @classmethod
    def detect(cls) -> bool:
        """Verifica se o binário do gestor está disponível no sistema."""
        return shutil.which(cls.executable_name) is not None

    @classmethod
    def get_version(cls) -> Optional[str]:
        """Obtém a versão instalada do gestor (se disponível)."""
        if not cls.detect():
            return None

        try:
            result = cls.command_executor.run(
                [cls.executable_name, *cls.version_args],
                timeout=cls.command_timeout,
            )
            output = result.stdout.strip() or result.stderr.strip()
            return output or None
        except (CommandTimeoutError, CommandExecutionError):
            return None

    @abstractmethod
    def list_packages(self) -> List[Dict[str, Any]]:
        """Retorna lista de pacotes instalados."""

    @abstractmethod
    def uninstall(self, package: str, force: bool = False) -> Dict[str, Any]:
        """Remove um pacote e devolve metadados sobre a operação."""

    @abstractmethod
    def export_manifest(self) -> Dict[str, Any]:
        """Exporta manifest/instantâneo no formato do gestor."""

    def get_dependency_tree(self, package: Optional[str] = None) -> Dict[str, Any]:
        """Obtém árvore de dependências de um pacote específico ou de todos.

        Implementação padrão retorna estrutura vazia. Subclasses devem sobrescrever.
        """
        return {
            "manager": self.manager_id,
            "package": package,
            "tree": {},
            "supported": False,
            "message": "Dependency tree not implemented for this manager",
        }

    def scan_vulnerabilities(self) -> Dict[str, Any]:
        """Escaneia vulnerabilidades conhecidas nos pacotes instalados.

        Implementação padrão retorna estrutura vazia. Subclasses devem sobrescrever.
        """
        return {
            "manager": self.manager_id,
            "vulnerabilities": [],
            "supported": False,
            "message": "Vulnerability scanning not implemented for this manager",
        }

    def export_lockfile(self) -> Dict[str, Any]:
        """Exporta lockfile do gestor de pacotes.

        Implementação padrão retorna estrutura vazia. Subclasses devem sobrescrever.
        """
        return {
            "manager": self.manager_id,
            "lockfile": {},
            "supported": False,
            "message": "Lockfile export not implemented for this manager",
        }

    # --- Utilitários de comandos -------------------------------------------------------

    def build_command(self, *args: str) -> List[str]:
        """Constroi comando base adicionando o executável do gestor."""
        return [self.executable_name, *args]

    def build_package_command(
        self,
        base_args: List[str],
        packages: List[str],
    ) -> List[str]:
        """Constroi comandos que incluem nomes de pacotes sanitizados."""
        sanitized = [self._sanitize_package(pkg) for pkg in packages]
        return [self.executable_name, *base_args, *sanitized]

    def run_command(
        self,
        args: List[str],
        *,
        timeout: Optional[int] = None,
        check: bool = True,
        cwd: Optional[str] = None,
    ):
        """Executa um comando síncrono através do CommandExecutor."""
        return self.command_executor.run(
            self.build_command(*args),
            timeout=timeout or self.command_timeout,
            check=check,
            cwd=cwd,
        )

    async def run_command_async(
        self,
        args: List[str],
        *,
        timeout: Optional[int] = None,
    ):
        """Executa comando de forma assíncrona."""
        return await self.command_executor.run_async(
            self.build_command(*args),
            timeout=timeout or self.command_timeout,
        )

    def _sanitize_package(self, package: str) -> str:
        """Sanitiza nome de pacote utilizando o ValidationLayer."""
        return ValidationLayer.sanitize_package_name(package)

    # --- Persistência auxiliar ---------------------------------------------------------

    def cache_write(self, name: str, data: Any) -> Path:
        """Grava dados no storage dedicado ao adapter."""
        return self.storage.write(self._adapter_storage_path(name), data)

    def cache_read(self, name: str) -> Any:
        """Lê dados do storage dedicado ao adapter."""
        return self.storage.read(self._adapter_storage_path(name))

    def cache_exists(self, name: str) -> bool:
        """Verifica se existe ficheiro no storage do adapter."""
        return self.storage.exists(self._adapter_storage_path(name))

    def cache_delete(self, name: str) -> bool:
        """Remove ficheiro do storage do adapter."""
        return self.storage.delete(self._adapter_storage_path(name))

    def _adapter_storage_path(self, relative_name: str) -> str:
        """Constrói caminho relativo seguro para o adapter."""
        clean_name = relative_name.lstrip("/")
        return str(Path("adapters") / self.manager_id / clean_name)
