"""Pydantic validation for Pint Quantities."""

from __future__ import annotations

try:
    from ._version import __version__
except ImportError:
    __version__ = "0.0"


__all__ = [
    "PydanticPintQuantity",
]

from .quantity import PydanticPintQuantity
