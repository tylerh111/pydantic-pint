from __future__ import annotations

import pytest
from pint.facets.plain import PlainQuantity
from pydantic import BaseModel, ValidationError

from pydantic_pint import PydanticPintQuantity, get_registry

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


def test_quantity_construction_unrestricted_nonstrict():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity(strict=False)]

    x = TestModel(value=1)
    assert x.value.m == 1
    assert x.value.u.dimensionless
    assert x.value == ureg("1")

    x = TestModel(value="1m")
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("1m")

    x = TestModel(value="1s")
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("s")
    assert x.value == ureg("1s")


def test_quantity_construction_unrestricted_strict():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity(strict=True)]

    with pytest.raises(ValidationError):
        TestModel(value=1)

    x = TestModel(value="1m")
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("1m")

    x = TestModel(value="1s")
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("s")
    assert x.value == ureg("1s")
