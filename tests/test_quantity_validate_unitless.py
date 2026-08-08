from __future__ import annotations

from pint.facets.plain import PlainQuantity
from pydantic import BaseModel

from pydantic_pint import PydanticPintQuantity, get_registry

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


def test_quantity_validate_unitless_number():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("%", strict=False)]

    x = TestModel(value=1)
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("%")
    assert x.value == ureg("1%")


def test_quantity_validate_unitless_dict():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("%")]

    x = TestModel(value={"magnitude": 1, "units": "percent"})
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("%")
    assert x.value == ureg("1%")


def test_quantity_validate_unitless_quantity():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("%")]

    x = TestModel(value=ureg("1%"))
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("%")
    assert x.value == ureg("1%")
