"""Interfaces e helpers para adapters de gestores de pacotes."""

from .base import BaseAdapter
from .brew import BrewAdapter
from .npm import NpmAdapter
from .pip import PipAdapter
from .pipx import PipxAdapter
from .pnpm import PnpmAdapter
from .registry import (
    REGISTERED_ADAPTERS,
    get_adapter_by_id,
    get_registered_adapters,
)
from .winget import WinGetAdapter

__all__ = [
    "BaseAdapter",
    "NpmAdapter",
    "PipAdapter",
    "PipxAdapter",
    "PnpmAdapter",
    "WinGetAdapter",
    "BrewAdapter",
    "REGISTERED_ADAPTERS",
    "get_registered_adapters",
    "get_adapter_by_id",
]
