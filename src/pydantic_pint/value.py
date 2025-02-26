"""Defines the Pydantic compatible wrapper for an instance of `pint.Quantity`."""

from __future__ import annotations

from numbers import Number

import pint
from pint.facets.plain.quantity import PlainQuantity as Quantity
from pydantic_core import core_schema, SchemaSerializer

from pydantic_pint.registry import get_registry


class PydanticPintValue:
    """Proxy class for a Pint Quantity instance.

    Unlink `PydanticPintQuantity`, `PydanticPintValue` wraps an instance of a pint quantity.
    Methods are added to allow it to interact with pydantic, e.g. serialization.
    The class immediately resolves to a `pint.Quantity` upon construction.
    The primary use for `PydanticPintValue` is in `pydantic.Field` comparison restrictions.

    Args:
        __value:
            The magnitude of the quantity.
        __units:
            The units of the quantity.
        ureg:
            A custom Pint unit registry.
    """

    def __new__(
        cls,
        __value: Number,
        __units: str | None = None,
        /,
        *,
        ureg: pint.UnitRegistry | None = None,
    ):
        ureg = ureg if ureg else get_registry()
        inst = ureg.Quantity(__value, __units)

        inst._pydantic_serialize = cls._pydantic_serialize
        inst.__pydantic_serializer__ = cls.__pydantic_serializer__

        return inst

    def _pydantic_serialize(
        self,
        v: Quantity,
        info: core_schema.SerializationInfo | None = None,
    ) -> str:
        return str(v)

    __pydantic_serializer__ = SchemaSerializer(
        core_schema.any_schema(
            serialization=core_schema.plain_serializer_function_ser_schema(
                _pydantic_serialize,
                info_arg=True,
                when_used='always',
            )
        )
    )
