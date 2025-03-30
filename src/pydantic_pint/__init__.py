"""Pydantic validation for Pint Quantities."""

from __future__ import annotations

try:
    from ._version import __version__
except ImportError:
    __version__ = "0.2"


__all__ = [
    "PydanticPintQuantity",
    "PydanticPintValue",
    "app_registry",
    "get_registry",
    "set_registry",
]

from .quantity import PydanticPintQuantity
from .registry import app_registry, get_registry, set_registry
from .value import PydanticPintValue
