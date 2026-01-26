"""Defines the Pydantic compatible wrapper for an instance of `pint.Quantity`."""

from __future__ import annotations

from numbers import Number

import pint
from pydantic_core import SchemaSerializer, core_schema

from pydantic_pint.registry import get_registry

__all__ = [
    "pydantic_pint_value",
]


def pydantic_pint_value(
    value: Number,
    units: str | None = None,
    /,
    *,
    ureg: pint.UnitRegistry | None = None,
) -> pint.Quantity:
    """Construct `pint.Quantity` with an injected Pydantic schema.

    A serialization schema is added to a Pint quantity to allow it to be serialized
    by pydantic. This in-turn allows Pint values to be used in a `pydantic.Field`
    context.

    Args:
        value (Number):
            The magnitude of the quantity.
        units (str | None, optional):
            The units of the quantity.
            Defaults to unitless quantity.
        ureg (pint.UnitRegistry | None, optional):
            The unit registry from which to create the quantity.
            Defaults to `pydantic_pint.app_registry`.

    Returns:
        A `pint.Quantity` with pydantic serialization.
    """
    ureg = ureg if ureg else get_registry()
    inst = ureg.Quantity(value, units)

    schema = SchemaSerializer(
        core_schema.any_schema(
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda v: str(v),
                info_arg=False,
                when_used="always",
            )
        )
    )

    setattr(inst, "__pydantic_serializer__", schema)

    return inst


# for compatibility
PydanticPintValue = pydantic_pint_value
"""Proxy class for a Pint Quantity instance with pydantic serialization.

!!! warning

    The name `PydanticPintQuantity` is deprecated. Use `pydantic_pint_value` instead.

Unlink `PydanticPintQuantity`, `PydanticPintValue` wraps an instance of a pint
quantity. Methods are added to allow it to interact with pydantic, e.g. serialization.
The class immediately resolves to a `pint.Quantity` upon construction. The primary
use for `PydanticPintValue` is in `pydantic.Field` comparison restrictions.

See `pydantic_pint_value` for more details.
"""
