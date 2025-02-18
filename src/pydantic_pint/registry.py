"""Defines the global unit registry for `PydanticPintQuantity`."""

from __future__ import annotations

import pint

_registry = pint.UnitRegistry()


def get_unit_registry() -> pint.UnitRegistry:
    """
    Returns the current unit registry to be used.
    Always use this function to retrieve the unit registry.
    """
    return _registry


def init_unit_registry(registry: pint.UnitRegistry) -> None:
    """
    Overrides the global unit registry with the provided registry.
    """
    global _registry
    _registry = registry
