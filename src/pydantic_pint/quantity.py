"""Defines the Pydantic `pint.Quantity`."""

from __future__ import annotations

from numbers import Number
from typing import TYPE_CHECKING, Any, Iterable, Literal

if TYPE_CHECKING:
    from pydantic import GetCoreSchemaHandler

import pint
from pint.facets.plain.quantity import PlainQuantity as Quantity
from pydantic_core import core_schema


class PydanticPintQuantity:
    """Pydantic Pint Quantity.

    Pydantic compatible annotation for validating and serializing `pint.Quantity` fields.

    Args:
        units:
            The base units of the Pydantic field.
            All input units must be convertible to these units.
        ureg:
            A custom Pint unit registry.
        ureg_contexts:
            A custom Pint context (or context name) for the default unit registry.
            All contexts are applied in validation conversion.
        ser_mode:
            The mode for serializing the field; either `"str"` or `"dict"`.
            By default, in Pydantic's `"python"` serialization mode, fields are serialzied to a `pint.Quantity`;
            in Pydantic's `"json"` serialziation mode, fields are serialized to a `str`.
        strict:
            Forces users to specify units; on by default.
            If disabled, a value without units - provided by the user - will be treated as the base units of the `PydanticPintQuantity`.
    """

    def __init__(
        self,
        units: str,
        *,
        ureg: pint.UnitRegistry | None = None,
        ureg_contexts: Iterable[str | pint.Context] | None = None,
        ser_mode: Literal["str", "dict"] | None = None,
        strict: bool = True,
    ):
        self.ser_mode = ser_mode.lower() if ser_mode else None
        self.strict = strict

        self.ureg = ureg if ureg else pint.UnitRegistry()
        self.ureg_contexts = ureg_contexts if ureg_contexts else []

        self.units = self.ureg(units)

    def validate(
        self,
        v: dict | str | Number | Quantity,
        info: core_schema.ValidationInfo | None = None,
    ) -> Quantity:
        """Validate `PydanticPintQuantity`.

        Args:
            v:
                The quantity that should be validated.
            info:
                The validation info provided by the Pydantic schema.

        Returns:
            The validated `pint.Quantity` with the correct units.

        Raises:
            ValueError:
                An error occurred validating the specified value.
                It is raised if any of the following occur.

                - A `dict` is received and the keys `"magnitude"` and `"units"` do not exist.
                - There are no units provided in strict mode.
                - Provided units cannot be converted to base units.
                - An unknown unit was provided.
                - An unknown type for value was provided.
            TypeError:
                An error occurred from unit registry or unit registry context.
                It is not propagated as a `pydantic.ValidationError` because it does not stem from a user error.
        """
        try:
            if isinstance(v, dict):
                v = f"{v['magnitude']} {v.get('units', '')}"
        except KeyError as e:
            raise ValueError("no `magnitude` or `units` keys found") from e

        try:
            if isinstance(v, str):
                # relies on ureg to return a number if no units are present
                # if value is a quantity, then units are present and check on the units being convertible
                # if value is a number, then check on strict mode will happen next
                v = self.ureg(v)
        except pint.UndefinedUnitError as e:
            raise ValueError(e) from e

        try:
            if isinstance(v, Number) and not self.strict:
                # check must happen after conversion from string because string might not have any units
                # only applicable if dealing with no units and if in strict mode
                v = v * self.units
            if isinstance(v, Quantity):
                v = v.to(self.units, *self.ureg_contexts)
                return v
        except AttributeError as e:
            # raises attribute error if value is a number
            # this case only happes when parsing from a string, the units are not present, and not in strict mode
            # see comments above related to ureg returning a number
            raise ValueError("no units found") from e
        except pint.DimensionalityError as e:
            raise ValueError(e) from e
        except KeyError as e:
            # this should not be considered a validation error
            # raising a type error with extra information
            raise TypeError(f"unknown unit registry context {e}") from e

        raise ValueError(f"unknown type {type(v)}")

    def serialize(
        self,
        v: Quantity,
        info: core_schema.SerializationInfo | None = None,
        *,
        to_json: bool = False,
    ) -> dict | str | Quantity:
        """Serialize `PydanticPintQuantity`.

        Args:
            v:
                The quantity that should be serialized.
            info:
                The serialization info provided by the Pydantic schema.
            to_json:
                Whether or not to serialize to a json convertible object.
                Useful if using `PydantiPintQuantity` as a utility outside of Pydantic models.

        Returns:
            The serialized `pint.Quantity`.
        """
        to_json = to_json or (info and info.mode_is_json())

        if self.ser_mode == "dict":
            return {
                "magnitude": v.magnitude,
                "units": v.units if not to_json else f"{v.units}",
            }

        if self.ser_mode == "str" or to_json:
            return f"{v}"

        return v

    def __get_pydantic_core_schema__(
        self,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        """Gets the Pydantic core schema.

        Args:
            source_type:
                The source type.
            handler:
                The `GetCoreSchemaHandler` instance.

        Returns:
            The Pydantic core schema.
        """
        _from_typedict_schema = {
            "magnitude": core_schema.typed_dict_field(
                core_schema.str_schema(coerce_numbers_to_str=True)
            ),
            "units": core_schema.typed_dict_field(core_schema.str_schema()),
        }

        validate_schema = core_schema.chain_schema(
            [
                core_schema.union_schema(
                    [
                        core_schema.is_instance_schema(Quantity),
                        core_schema.str_schema(coerce_numbers_to_str=True),
                        core_schema.typed_dict_schema(_from_typedict_schema),
                    ]
                ),
                core_schema.with_info_plain_validator_function(self.validate),
            ]
        )

        validate_json_schema = core_schema.chain_schema(
            [
                core_schema.union_schema(
                    [
                        core_schema.str_schema(coerce_numbers_to_str=True),
                        core_schema.typed_dict_schema(_from_typedict_schema),
                    ]
                ),
                core_schema.no_info_plain_validator_function(self.validate),
            ]
        )

        serialize_schema = core_schema.plain_serializer_function_ser_schema(
            self.serialize,
            info_arg=True,
        )

        return core_schema.json_or_python_schema(
            json_schema=validate_json_schema,
            python_schema=validate_schema,
            serialization=serialize_schema,
        )
