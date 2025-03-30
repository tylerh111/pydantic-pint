"""Defines the global unit registry for `PydanticPintQuantity`."""

from __future__ import annotations

import pint

__all__ = [
    "app_registry",
    "get_registry",
    "set_registry",
]


_DEFAULT_REGISTRY = pint.LazyRegistry()

app_registry = pint.ApplicationRegistry(_DEFAULT_REGISTRY)
"""Pydantic Pint default application registry."""


def get_registry() -> pint.UnitRegistry:
    """Get the Pydantic Pint global registry.

    Returns:
        The current global registry.
    """
    return app_registry.get()


def set_registry(registry: pint.UnitRegistry):
    """Set the Pydantic Pint global registry.

    Args:
        registry: The new global registry.
    """
    app_registry.set(registry)
