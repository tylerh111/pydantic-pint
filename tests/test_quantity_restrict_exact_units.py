from __future__ import annotations

import pytest
from pint.facets.plain import PlainQuantity
from pydantic import BaseModel, ValidationError

from pydantic_pint import PydanticPintQuantity, get_registry

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


def test_quantity_restrict_nonstrict_nonexact_units():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[
            PlainQuantity, PydanticPintQuantity("m", strict=False, exact=False)
        ]

    x = TestModel(value=1)
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("1m")

    x = TestModel(value="1m")
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("1m")

    x = TestModel(value="1km")
    assert x.value.m == 1000
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("1000m")


def test_quantity_restrict_strict_nonexact_units():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[
            PlainQuantity, PydanticPintQuantity("m", strict=True, exact=False)
        ]

    with pytest.raises(ValidationError):
        TestModel(value=1)

    x = TestModel(value="1m")
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("1m")

    x = TestModel(value="1km")
    assert x.value.m == 1000
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("1000m")


def test_quantity_restrict_nonstrict_exact_units():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[
            PlainQuantity, PydanticPintQuantity("m", strict=False, exact=True)
        ]

    x = TestModel(value=1)
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("1m")

    x = TestModel(value="1m")
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("1m")

    with pytest.raises(ValidationError):
        TestModel(value="1km")


def test_quantity_restrict_strict_exact_units():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[
            PlainQuantity, PydanticPintQuantity("m", strict=True, exact=True)
        ]

    with pytest.raises(ValidationError):
        TestModel(value=1)

    x = TestModel(value="1m")
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("1m")

    with pytest.raises(ValidationError):
        TestModel(value="1km")
