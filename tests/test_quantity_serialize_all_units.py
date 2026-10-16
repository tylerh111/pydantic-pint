from __future__ import annotations

import math
from importlib.metadata import version

import pytest
from packaging.version import Version

from pydantic_pint import PydanticPintQuantity, get_registry


MAGNITUDE = 42.0
ureg = get_registry()

# Non-multiplicative units (offset and logarithmic) fail to validate correctly
# in pint<0.26 due to pint [#386](https://github.com/hgrecco/pint/issues/386)
# and fixed in pint [#2300](https://github.com/hgrecco/pint/pull/2300).
skip_non_multiplicative = pytest.mark.skipif(
    Version(version("pint")) < Version("0.26"),
    reason="non-multiplicative units are broken in pint<0.26",
)


def _check_equality(expected, actual):
    assert math.isclose(actual.magnitude, expected.magnitude)
    assert actual.units == expected.units


# This unit test is parametrized by the available units defined by default in pint.
# All non-base units are tested against their reference units.
# For more information, find defintions file `pint/default_en.txt`.
@pytest.mark.parametrize(
    "unit",
    [
        pytest.param(
            unit,
            marks=() if unitdef.is_multiplicative else skip_non_multiplicative,
        )
        for unit, unitdef in ureg._units.items()
        if not unitdef.is_base
    ],
)
def test_quantity_serialize_all_units(unit: str):
    unitdef = ureg._units[unit]

    validator = PydanticPintQuantity(unitdef.name, strict=True)
    validator_nonstrict = PydanticPintQuantity(unitdef.name, strict=False)

    expected = ureg.Quantity(MAGNITUDE, unitdef.name)

    validator.ser_mode = None
    actual = validator.validate(validator.serialize(expected))
    _check_equality(expected, actual)
    validator.ser_mode = "str"
    actual = validator.validate(validator.serialize(expected))
    _check_equality(expected, actual)
    validator.ser_mode = "dict"
    actual = validator.validate(validator.serialize(expected))
    _check_equality(expected, actual)
    validator_nonstrict.ser_mode = "number"
    actual = validator_nonstrict.validate(validator.serialize(expected))
    _check_equality(expected, actual)

    if unitdef.reference == ureg.dimensionless:
        expected = ureg.Quantity(MAGNITUDE, unitdef.name)
    else:
        expected = ureg.Quantity(
            unitdef.converter.from_reference(MAGNITUDE), unitdef.name
        )

    validator.ser_mode = None
    actual = validator.validate(validator.serialize(expected))
    _check_equality(expected, actual)
    validator.ser_mode = "str"
    actual = validator.validate(validator.serialize(expected))
    _check_equality(expected, actual)
    validator.ser_mode = "dict"
    actual = validator.validate(validator.serialize(expected))
    _check_equality(expected, actual)
    validator_nonstrict.ser_mode = "number"
    actual = validator_nonstrict.validate(validator.serialize(expected))
    _check_equality(expected, actual)
