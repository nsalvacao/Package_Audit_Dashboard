"""Routers FastAPI."""

from . import advanced, discover, health, managers, packages, streaming

__all__ = ["discover", "managers", "packages", "streaming", "advanced", "health"]
