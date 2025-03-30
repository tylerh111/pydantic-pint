from __future__ import annotations

from pint.facets.plain import PlainQuantity
from pydantic import BaseModel

from pydantic_pint import PydanticPintQuantity, get_registry

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


def test_quantity_compare_metric_prefixes_1Tm():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m")]

    x = TestModel(value="1Tm")
    assert x.value.m == 1000000000000
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("1000000000000m")


def test_quantity_compare_metric_prefixes_1Gm():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m")]

    x = TestModel(value="1Gm")
    assert x.value.m == 1000000000
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("1000000000m")


def test_quantity_compare_metric_prefixes_1Mm():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m")]

    x = TestModel(value="1Mm")
    assert x.value.m == 1000000
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("1000000m")


def test_quantity_compare_metric_prefixes_1km():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m")]

    x = TestModel(value="1km")
    assert x.value.m == 1000
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("1000m")


def test_quantity_compare_metric_prefixes_1hm():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m")]

    x = TestModel(value="1hm")
    assert x.value.m == 100
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("100m")


def test_quantity_compare_metric_prefixes_1dam():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m")]

    x = TestModel(value="1dam")
    assert x.value.m == 10
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("10m")


def test_quantity_compare_metric_prefixes_1m():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m")]

    x = TestModel(value="1m")
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("1m")


def test_quantity_compare_metric_prefixes_1dm():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m")]

    x = TestModel(value="1dm")
    assert x.value.m == 0.1
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("0.1m")


def test_quantity_compare_metric_prefixes_1cm():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m")]

    x = TestModel(value="1cm")
    assert x.value.m == 0.01
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("0.01m")


def test_quantity_compare_metric_prefixes_1mm():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m")]

    x = TestModel(value="1mm")
    assert x.value.m == 0.001
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("0.001m")


def test_quantity_compare_metric_prefixes_1μm():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m")]

    x = TestModel(value="1μm")
    assert x.value.m == 0.000001
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("0.000001m")


def test_quantity_compare_metric_prefixes_1nm():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m")]

    x = TestModel(value="1nm")
    assert x.value.m == 0.000000001
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("0.000000001m")


def test_quantity_compare_metric_prefixes_1pm():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m")]

    x = TestModel(value="1pm")
    assert x.value.m == 0.000000000001
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("0.000000000001m")
