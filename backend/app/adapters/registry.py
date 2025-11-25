"""Registo centralizado dos adapters disponíveis."""
from __future__ import annotations

from typing import List, Optional, Type

from .base import BaseAdapter
from .brew import BrewAdapter
from .npm import NpmAdapter
from .pip import PipAdapter
from .pipx import PipxAdapter
from .pnpm import PnpmAdapter
from .winget import WinGetAdapter

REGISTERED_ADAPTERS: List[Type[BaseAdapter]] = [
    NpmAdapter,
    PipAdapter,
    WinGetAdapter,
    BrewAdapter,
    PipxAdapter,
    PnpmAdapter,
]


def get_registered_adapters() -> List[Type[BaseAdapter]]:
    """Retorna lista de adapters registados."""
    return REGISTERED_ADAPTERS


def get_adapter_by_id(manager_id: str) -> Optional[Type[BaseAdapter]]:
    """Obtém adapter correspondente ao identificador, se existir."""
    for adapter in REGISTERED_ADAPTERS:
        if adapter.manager_id == manager_id:
            return adapter
    return None
