"""Pydantic validation for Pint Quantities."""

from __future__ import annotations

try:
    from ._version import __version__
except ImportError:
    __version__ = "0.1"


__all__ = [
    "get_unit_registry",
    "init_unit_registry",
    "PydanticPintQuantity",
]

from .quantity import PydanticPintQuantity
from .registry import get_unit_registry, init_unit_registry
