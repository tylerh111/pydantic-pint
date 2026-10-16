from __future__ import annotations

from pint.facets.plain import PlainQuantity
from pydantic import BaseModel

from pydantic_pint import PydanticPintQuantity, get_registry

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


def test_quantity_restrict_dimensionless_restrict_units_number():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("dimensionless")]

    x = TestModel(value=1)
    assert x.value.m == 1
    assert x.value.u == ureg.dimensionless
    assert x.value == ureg("1 dimensionless")


def test_quantity_restrict_dimensionless_restrict_units_str():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("dimensionless")]

    x = TestModel(value="1")
    assert x.value.m == 1
    assert x.value.u == ureg.dimensionless
    assert x.value == ureg("1 dimensionless")

    x = TestModel(value="1 dimensionless")
    assert x.value.m == 1
    assert x.value.u == ureg.dimensionless
    assert x.value == ureg("1 dimensionless")


def test_quantity_restrict_dimensionless_restrict_units_dict():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("dimensionless")]

    x = TestModel(value={"magnitude": 1})
    assert x.value.m == 1
    assert x.value.u == ureg.dimensionless
    assert x.value == ureg("1 dimensionless")

    x = TestModel(value={"magnitude": 1, "units": "dimensionless"})
    assert x.value.m == 1
    assert x.value.u == ureg.dimensionless
    assert x.value == ureg("1 dimensionless")


def test_quantity_restrict_dimensionless_restrict_units_quantity():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("dimensionless")]

    x = TestModel(value=ureg("1"))
    assert x.value.m == 1
    assert x.value.u == ureg.dimensionless
    assert x.value == ureg("1 dimensionless")

    x = TestModel(value=ureg("1 dimensionless"))
    assert x.value.m == 1
    assert x.value.u == ureg.dimensionless
    assert x.value == ureg("1 dimensionless")


def test_quantity_restrict_dimensionless_restrict_dimensions_number():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[
            PlainQuantity, PydanticPintQuantity("", restriction="dimensions")
        ]

    x = TestModel(value=1)
    assert x.value.m == 1
    assert x.value.u == ureg.dimensionless
    assert x.value == ureg("1 dimensionless")


def test_quantity_restrict_dimensionless_restrict_dimensions_str():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[
            PlainQuantity, PydanticPintQuantity("", restriction="dimensions")
        ]

    x = TestModel(value="1")
    assert x.value.m == 1
    assert x.value.u == ureg.dimensionless
    assert x.value == ureg("1 dimensionless")

    x = TestModel(value="1 dimensionless")
    assert x.value.m == 1
    assert x.value.u == ureg.dimensionless
    assert x.value == ureg("1 dimensionless")


def test_quantity_restrict_dimensionless_restrict_dimensions_dict():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[
            PlainQuantity, PydanticPintQuantity("", restriction="dimensions")
        ]

    x = TestModel(value={"magnitude": 1})
    assert x.value.m == 1
    assert x.value.u == ureg.dimensionless
    assert x.value == ureg("1 dimensionless")

    x = TestModel(value={"magnitude": 1, "units": "dimensionless"})
    assert x.value.m == 1
    assert x.value.u == ureg.dimensionless
    assert x.value == ureg("1 dimensionless")


def test_quantity_restrict_dimensionless_restrict_dimensions_quantity():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[
            PlainQuantity, PydanticPintQuantity("", restriction="dimensions")
        ]

    x = TestModel(value=ureg("1"))
    assert x.value.m == 1
    assert x.value.u == ureg.dimensionless
    assert x.value == ureg("1 dimensionless")

    x = TestModel(value=ureg("1 dimensionless"))
    assert x.value.m == 1
    assert x.value.u == ureg.dimensionless
    assert x.value == ureg("1 dimensionless")
