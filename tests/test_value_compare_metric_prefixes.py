
from __future__ import annotations

from pydantic_pint import PydanticPintValue, get_registry


def test_value_compare_1Tm():

    ureg = get_registry()

    value = PydanticPintValue(1, "Tm")
    assert value.m == 1
    assert value.u == ureg.Unit("Tm")
    assert value.to("m") == ureg("1000000000000m")
    assert value == ureg("1Tm")


def test_value_compare_1Gm():

    ureg = get_registry()

    value = PydanticPintValue(1, "Gm")
    assert value.m == 1
    assert value.u == ureg.Unit("Gm")
    assert value.to("m") == ureg("1000000000m")
    assert value == ureg("1Gm")


def test_value_compare_1Mm():

    ureg = get_registry()

    value = PydanticPintValue(1, "Mm")
    assert value.m == 1
    assert value.u == ureg.Unit("Mm")
    assert value.to("m") == ureg("1000000m")
    assert value == ureg("1Mm")


def test_value_compare_1km():

    ureg = get_registry()

    value = PydanticPintValue(1, "km")
    assert value.m == 1
    assert value.u == ureg.Unit("km")
    assert value.to("m") == ureg("1000m")
    assert value == ureg("1km")


def test_value_compare_1hm():

    ureg = get_registry()

    value = PydanticPintValue(1, "hm")
    assert value.m == 1
    assert value.u == ureg.Unit("hm")
    assert value.to("m") == ureg("100m")
    assert value == ureg("1hm")


def test_value_compare_1dam():

    ureg = get_registry()

    value = PydanticPintValue(1, "dam")
    assert value.m == 1
    assert value.u == ureg.Unit("dam")
    assert value.to("m") == ureg("10m")
    assert value == ureg("1dam")


def test_value_compare_1m():

    ureg = get_registry()

    value = PydanticPintValue(1, "m")
    assert value.m == 1
    assert value.u == ureg.Unit("m")
    assert value.to("m") == ureg("1m")
    assert value == ureg("1m")


def test_value_compare_1dm():

    ureg = get_registry()

    value = PydanticPintValue(1, "dm")
    assert value.m == 1
    assert value.u == ureg.Unit("dm")
    assert value.to("m") == ureg("0.1m")
    assert value == ureg("1dm")


def test_value_compare_1cm():

    ureg = get_registry()

    value = PydanticPintValue(1, "cm")
    assert value.m == 1
    assert value.u == ureg.Unit("cm")
    assert value.to("m") == ureg("0.01m")
    assert value == ureg("1cm")


def test_value_compare_1mm():

    ureg = get_registry()

    value = PydanticPintValue(1, "mm")
    assert value.m == 1
    assert value.u == ureg.Unit("mm")
    assert value.to("m") == ureg("0.001m")
    assert value == ureg("1mm")


def test_value_compare_1μm():

    ureg = get_registry()

    value = PydanticPintValue(1, "μm")
    assert value.m == 1
    assert value.u == ureg.Unit("μm")
    assert value.to("m") == ureg("0.000001m")
    assert value == ureg("1μm")


def test_value_compare_1nm():

    ureg = get_registry()

    value = PydanticPintValue(1, "nm")
    assert value.m == 1
    assert value.u == ureg.Unit("nm")
    assert value.to("m") == ureg("0.000000001m")
    assert value == ureg("1nm")


def test_value_compare_1pm():

    ureg = get_registry()

    value = PydanticPintValue(1, "pm")
    assert value.m == 1
    assert value.u == ureg.Unit("pm")
    assert value.to("m") == ureg("0.000000000001m")
    assert value == ureg("1pm")
