
from __future__ import annotations

import pytest
from pint.facets.plain import PlainQuantity
from pydantic import BaseModel, ValidationError
from pydantic_pint import PydanticPintQuantity, get_registry

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


def test_quantity_restrict_nonstrict_units_1m():

    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m", strict=False)]

    x = TestModel(value=1)
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("1m")


def test_quantity_restrict_nonstrict_units_1km():

    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("km", strict=False)]

    x = TestModel(value=1)
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("km")
    assert x.value == ureg("1km")


def test_quantity_restrict_strict_units_1m():

    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m", strict=True)]

    x = TestModel(value="1m")
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("1m")

    with pytest.raises(ValidationError):
        TestModel(value=1)


def test_quantity_restrict_strict_units_1km():

    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("km", strict=True)]

    x = TestModel(value="1km")
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("km")
    assert x.value == ureg("1km")

    with pytest.raises(ValidationError):
        TestModel(value=1)
