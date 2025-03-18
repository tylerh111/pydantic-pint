
from __future__ import annotations

import pytest
from pint import Context, UnitRegistry
from pint.facets.plain import PlainQuantity
from pydantic import BaseModel, ValidationError
from pydantic_pint import PydanticPintQuantity

from typing_extensions import Annotated


def test_quantity_custom_unit_registry():

    ureg = UnitRegistry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m", ureg=ureg)]

    x = TestModel(value="1m", ureg=ureg)
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("1m")


def test_quantity_custom_unit_registry_with_custom_transformations():

    ureg = UnitRegistry()
    ctx = Context()
    ctx.add_transformation("[length]", "[time]", lambda ureg, x: x / (100 * ureg.miles) * (1.5 * ureg.hours))
    ctx.add_transformation("[time]", "[length]", lambda ureg, x: x / (1.5 * ureg.hours) * (100 * ureg.miles))
    ureg.enable_contexts(ctx)

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("hr", ureg=ureg)]

    x = TestModel(value="100mi")
    assert x.value.m == 1.5
    assert x.value.u == ureg.Unit("hr")
    assert x.value == ureg("1.5hr")

    x = TestModel(value="1.5hr")
    assert x.value.m == 1.5
    assert x.value.u == ureg.Unit("hr")
    assert x.value == ureg("1.5hr")


def test_quantity_custom_unit_registry_with_custom_transformations_context_switch():

    ureg = UnitRegistry()
    ctx = Context()
    ctx.add_transformation("[length]", "[time]", lambda ureg, x: x / (100 * ureg.miles) * (1.5 * ureg.hours))
    ctx.add_transformation("[time]", "[length]", lambda ureg, x: x / (1.5 * ureg.hours) * (100 * ureg.miles))

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("hr", ureg=ureg)]

    with ureg.context(ctx):
        x = TestModel(value="100mi")
        assert x.value.m == 1.5
        assert x.value.u == ureg.Unit("hr")
        assert x.value == ureg("1.5hr")

        x = TestModel(value="1.5hr")
        assert x.value.m == 1.5
        assert x.value.u == ureg.Unit("hr")
        assert x.value == ureg("1.5hr")

    # fails when outside context block
    with pytest.raises(ValidationError):
        TestModel(value="100mi")
