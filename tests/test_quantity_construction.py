
from __future__ import annotations

import pytest
from pint.facets.plain import PlainQuantity
from pydantic import BaseModel, ValidationError
from pydantic_pint import PydanticPintQuantity, get_registry

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


def test_quantity_construction_number_nonstrict():

    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m", strict=False)]

    x = TestModel(value=1)
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("1m")


def test_quantity_construction_number_strict():

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m", strict=True)]

    with pytest.raises(ValidationError):
        TestModel(value=1)


def test_quantity_construction_str_nonstrict():

    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m", strict=False)]

    x = TestModel(value="1m")
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("1m")

    x = TestModel(value="1")
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("1m")


def test_quantity_construction_str_strict():

    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m", strict=True)]

    x = TestModel(value="1m")
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("1m")

    with pytest.raises(ValidationError):
        TestModel(value="1")


def test_quantity_construction_dict_nonstrict():

    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m", strict=False)]

    x = TestModel(value={"magnitude": 1, "units": "m"})
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("1m")

    x = TestModel(value={"magnitude": 1})
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("1m")


def test_quantity_construction_dict_strict():

    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m", strict=True)]

    x = TestModel(value={"magnitude": 1, "units": "m"})
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("1m")


    with pytest.raises(ValidationError):
        TestModel(value={"magnitude": 1})
