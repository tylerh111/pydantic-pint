"""Defines the Pydantic compatible wrapper for an instance of `pint.Quantity`."""

from __future__ import annotations

import sys
from numbers import Number

if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated

import pint
from pydantic_core import SchemaSerializer, core_schema

from pydantic_pint.registry import get_registry

__all__ = [
    "pydantic_pint_value",
    "pydantic_pint_value_schema",
    "inject_pydantic_schema",
]


def pydantic_pint_value_schema() -> SchemaSerializer:
    """The schema that can serialize a `pint.Quantity`.

    Returns:
        The serializer schema for Pydantic.
    """
    return SchemaSerializer(
        core_schema.any_schema(
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda v: str(v),
                info_arg=False,
                when_used="always",
            )
        )
    )


def inject_pydantic_schema(
    quantity: pint.Quantity,
) -> pint.Quantity:
    """Adds the Pydantic serializer schema to a Pint quantity.

    Args:
        quantity: The Pint quantity.

    Returns:
        The same Pint quantity with a pydantic schema.
    """
    setattr(
        quantity,
        "__pydantic_serializer__",
        pydantic_pint_value_schema(),
    )

    return quantity


def pydantic_pint_value(
    value: Number,
    units: str | None = None,
    /,
    *,
    ureg: pint.UnitRegistry | None = None,
) -> pint.Quantity:
    """Construct `pint.Quantity` with an injected Pydantic serialization schema.

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
    return inject_pydantic_schema(inst)


@deprecated("use `pydantic_pint_value` instead")
def PydanticPintValue(*args, **kwargs) -> pint.Quantity:
    """Proxy class for a Pint Quantity instance with pydantic serialization.

    !!! warning

        The name `PydanticPintQuantity` is deprecated. Use `pydantic_pint_value` instead.

    Unlike `PydanticPintQuantity`, `PydanticPintValue` wraps an instance of a pint
    quantity. Methods are added to allow it to interact with pydantic, e.g. serialization.
    The class immediately resolves to a `pint.Quantity` upon construction. The primary
    use for `PydanticPintValue` is in `pydantic.Field` comparison restrictions.

    See `pydantic_pint_value` for more details.
    """
    return pydantic_pint_value(*args, **kwargs)
