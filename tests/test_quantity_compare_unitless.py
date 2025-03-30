
from __future__ import annotations

import pytest
from pint.facets.plain import PlainQuantity
from pydantic import BaseModel, ValidationError
from pydantic_pint import PydanticPintQuantity, get_registry

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


def test_quantity_compare_unitless_nonstrict_nonexact():

    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("%", strict=False, exact=False)]

    x = TestModel(value=1)
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("%")
    assert x.value == ureg("1%")

    x = TestModel(value="1%")
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("%")
    assert x.value == ureg("1%")

    x = TestModel(value="1bit")
    assert x.value.m == 100
    assert x.value.u == ureg.Unit("%")
    assert x.value == ureg("100%")


def test_quantity_compare_unitless_nonstrict_exact():

    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("%", strict=False, exact=True)]

    x = TestModel(value=1)
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("%")
    assert x.value == ureg("1%")

    x = TestModel(value="1%")
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("%")
    assert x.value == ureg("1%")

    with pytest.raises(ValidationError):
        TestModel(value="1bit")


def test_quantity_compare_unitless_strict_nonexact():

    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("%", strict=True, exact=False)]

    with pytest.raises(ValidationError):
        TestModel(value=1)

    x = TestModel(value="1%")
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("%")
    assert x.value == ureg("1%")

    x = TestModel(value="1bit")
    assert x.value.m == 100
    assert x.value.u == ureg.Unit("%")
    assert x.value == ureg("100%")



def test_quantity_compare_unitless_strict_exact():

    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("%", strict=True, exact=True)]

    with pytest.raises(ValidationError):
        TestModel(value=1)

    x = TestModel(value="1%")
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("%")
    assert x.value == ureg("1%")

    with pytest.raises(ValidationError):
        TestModel(value="1bit")
