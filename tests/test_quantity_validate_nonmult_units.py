from __future__ import annotations

import pytest
from pint.facets.plain import PlainQuantity
from pydantic import BaseModel, ValidationError

from pydantic_pint import PydanticPintQuantity, get_registry

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


def test_quantity_validate_nonmult_units_degF():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("degF", strict=False)]

    x = TestModel(value=1)
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("degF")
    assert x.value == ureg.Quantity(1, "degF")

def test_quantity_validate_nonmult_units_degC():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("degC", strict=False)]

    x = TestModel(value=1)
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("degC")
    assert x.value == ureg.Quantity(1, "degC")
