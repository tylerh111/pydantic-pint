"""Defines the Pydantic compatible wrapper for an instance of `pint.Quantity`."""

from __future__ import annotations

from numbers import Number

import pint
from pydantic_core import SchemaSerializer, core_schema

from pydantic_pint.registry import get_registry


class PydanticPintValue:
    """Proxy class for a Pint Quantity instance with pydantic serialization.

    Unlink `PydanticPintQuantity`, `PydanticPintValue` wraps an instance of a pint quantity.
    Methods are added to allow it to interact with pydantic, e.g. serialization.
    The class immediately resolves to a `pint.Quantity` upon construction.
    The primary use for `PydanticPintValue` is in `pydantic.Field` comparison restrictions.
    """

    def __new__(
        cls,
        __value: Number,
        __units: str | None = None,
        /,
        *,
        ureg: pint.UnitRegistry | None = None,
    ) -> pint.Quantity:
        """Coarse value into a `pint.Quantity` based on provided unit registry.

        Args:
            __value (Number):
                The magnitude of the quantity.
            __units (str | None, optional):
                The units of the quantity.
                Defaults to unitless quantity.
            ureg (pint.UnitRegistry | None, optional):
                The unit registry from which to create the quantity.
                Defaults to `pydantic_pint.app_registry`.

        Returns:
            A `pint.Quantity` with pydantic serialization.
        """
        ureg = ureg if ureg else get_registry()
        inst = ureg.Quantity(__value, __units)

        inst.__pydantic_serializer__ = SchemaSerializer(
            core_schema.any_schema(
                serialization=core_schema.plain_serializer_function_ser_schema(
                    lambda v: str(v),
                    info_arg=False,
                    when_used="always",
                )
            )
        )

        return inst
