from __future__ import annotations

from pydantic_pint import PydanticPintValue, get_registry


def test_value_compare_1percent():
    ureg = get_registry()

    value = PydanticPintValue(1, "percent")
    assert value.m == 1
    assert value.u == ureg.Unit("%")
    assert value.to("percent") == ureg("1%")
    assert value == ureg("1%")


def test_value_compare_1bit():
    ureg = get_registry()

    value = PydanticPintValue(1, "bit")
    assert value.m == 1
    assert value.u == ureg.Unit("bit")
    assert value.to("percent") == ureg("100%")
    assert value == ureg("100%")
