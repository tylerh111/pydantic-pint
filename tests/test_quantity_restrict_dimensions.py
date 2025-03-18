
from __future__ import annotations

import pytest
from pint import Context, UnitRegistry
from pint.facets.plain import PlainQuantity
from pydantic import BaseModel, ValidationError
from pydantic_pint import PydanticPintQuantity, get_registry

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


def test_quantity_restrict_dimensions_length_input_string():

    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("[length]")]

    x = TestModel(value="1m")
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("m")
    assert x.value == ureg("1m")

    x = TestModel(value="1km")
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("km")
    assert x.value == ureg("1km")

    x = TestModel(value="1mm")
    assert x.value.m == 1
    assert x.value.u == ureg.Unit("mm")
    assert x.value == ureg("1mm")


def test_quantity_restrict_dimensions_length_input_number():

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("[length]")]

    with pytest.raises(ValidationError):
        TestModel(value=1)


def test_quantity_restrict_dimensions_length_input_incorrect_dimension():

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("[length]")]

    with pytest.raises(ValidationError):
        TestModel(value="1s")

    with pytest.raises(ValidationError):
        TestModel(value="1ms")


def test_quantity_restrict_dimensions_length_input_with_custom_transformations_nonexact():

    ureg = UnitRegistry()
    ctx = Context()
    ctx.add_transformation("[length]", "[time]", lambda ureg, x: x / (100 * ureg.miles) * (1.5 * ureg.hours))
    ctx.add_transformation("[time]", "[length]", lambda ureg, x: x / (1.5 * ureg.hours) * (100 * ureg.miles))
    ureg.enable_contexts(ctx)

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("[length]", exact=False, ureg=ureg)]

    x = TestModel(value="100mi")
    assert x.value.m == 100
    assert x.value.u == ureg.Unit("mi")
    assert x.value == ureg("100mi")

    x = TestModel(value="1.5hr")
    assert x.value.m == 1.5
    assert x.value.u == ureg.Unit("hr")
    assert x.value == ureg("1.5hr")


def test_quantity_restrict_dimensions_length_input_with_custom_transformations_exact():

    ureg = UnitRegistry()
    ctx = Context()
    ctx.add_transformation("[length]", "[time]", lambda ureg, x: x / (100 * ureg.miles) * (1.5 * ureg.hours))
    ctx.add_transformation("[time]", "[length]", lambda ureg, x: x / (1.5 * ureg.hours) * (100 * ureg.miles))
    ureg.enable_contexts(ctx)

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("[length]", exact=True, ureg=ureg)]

    x = TestModel(value="100mi")
    assert x.value.m == 100
    assert x.value.u == ureg.Unit("mi")
    assert x.value == ureg("100mi")

    with pytest.raises(ValidationError):
        TestModel(value="1.5hr")
