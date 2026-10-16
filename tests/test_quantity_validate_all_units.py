from __future__ import annotations

import math

import pytest

from pydantic_pint import PydanticPintQuantity, get_registry

MAGNITUDE = 42.0
ureg = get_registry()


def _check_equality(expected, actual):
    assert math.isclose(actual.magnitude, expected.magnitude)
    assert actual.units == expected.units


# This unit test is parametrized by the available units defined by default in pint.
# All non-base units are tested against their reference units.
# For more information, find defintions file `pint/default_en.txt`.
@pytest.mark.parametrize(
    "unit",
    [
        unit
        for unit, unitdef in ureg._units.items()
        if unitdef.name not in ureg._base_units
    ],
)
def test_quantity_serialize_all_units(unit: str):
    unitdef = ureg._units[unit]

    validator = PydanticPintQuantity(unitdef.name, strict=True)
    validator_nonstrict = PydanticPintQuantity(unitdef.name, strict=False)

    expected = ureg.Quantity(MAGNITUDE, unitdef.name)
    actual = validator.validate({"magnitude": MAGNITUDE, "units": unitdef.name})
    _check_equality(expected, actual)

    if unitdef.reference == ureg.dimensionless:
        expected = ureg.Quantity(MAGNITUDE, unitdef.name)
        actual = validator_nonstrict.validate(
            {"magnitude": MAGNITUDE, "units": unitdef.reference}
        )
    else:
        expected = ureg.Quantity(
            unitdef.converter.from_reference(MAGNITUDE), unitdef.name
        )
        actual = validator.validate(
            {"magnitude": MAGNITUDE, "units": unitdef.reference}
        )
    _check_equality(expected, actual)
