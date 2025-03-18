
from __future__ import annotations

import pytest
from pint.facets.plain import PlainQuantity
from pydantic import BaseModel, ValidationError, Field
from pydantic_pint import PydanticPintQuantity, PydanticPintValue, get_registry

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


def test_quantity_additional_annotations_field_gt():

    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m", strict=False), Field(gt=PydanticPintValue(0, "m", ureg=ureg))]

    # positive
    assert TestModel(value=1).value == ureg("1m")
    assert TestModel(value="1m").value == ureg("1m")
    assert TestModel(value="1km").value == ureg("1km")
    assert TestModel(value="1cm").value == ureg("1cm")

    # zero
    with pytest.raises(ValidationError): TestModel(value=0)
    with pytest.raises(ValidationError): TestModel(value="0m")
    with pytest.raises(ValidationError): TestModel(value="0km")
    with pytest.raises(ValidationError): TestModel(value="0cm")

    # negative
    with pytest.raises(ValidationError): TestModel(value=-1)
    with pytest.raises(ValidationError): TestModel(value="-1m")
    with pytest.raises(ValidationError): TestModel(value="-1km")
    with pytest.raises(ValidationError): TestModel(value="-1cm")

def test_quantity_additional_annotations_field_ge():

    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m", strict=False), Field(ge=PydanticPintValue(0, "m", ureg=ureg))]

    # positive
    assert TestModel(value=1).value == ureg("1m")
    assert TestModel(value="1m").value == ureg("1m")
    assert TestModel(value="1km").value == ureg("1km")
    assert TestModel(value="1cm").value == ureg("1cm")

    # zero
    assert TestModel(value=0).value == ureg("0m")
    assert TestModel(value="0m").value == ureg("0m")
    assert TestModel(value="0km").value == ureg("0km")
    assert TestModel(value="0cm").value == ureg("0cm")

    # negative
    with pytest.raises(ValidationError): TestModel(value=-1)
    with pytest.raises(ValidationError): TestModel(value="-1m")
    with pytest.raises(ValidationError): TestModel(value="-1km")
    with pytest.raises(ValidationError): TestModel(value="-1cm")

def test_quantity_additional_annotations_field_le():

    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m", strict=False), Field(le=PydanticPintValue(0, "m", ureg=ureg))]

    # positive
    with pytest.raises(ValidationError): TestModel(value=1)
    with pytest.raises(ValidationError): TestModel(value="1m")
    with pytest.raises(ValidationError): TestModel(value="1km")
    with pytest.raises(ValidationError): TestModel(value="1cm")

    # zero
    assert TestModel(value=0).value == ureg("0m")
    assert TestModel(value="0m").value == ureg("0m")
    assert TestModel(value="0km").value == ureg("0km")
    assert TestModel(value="0cm").value == ureg("0cm")

    # negative
    assert TestModel(value=-1).value == ureg("-1m")
    assert TestModel(value="-1m").value == ureg("-1m")
    assert TestModel(value="-1km").value == ureg("-1km")
    assert TestModel(value="-1cm").value == ureg("-1cm")

def test_quantity_additional_annotations_field_lt():

    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m", strict=False), Field(lt=PydanticPintValue(0, "m", ureg=ureg))]

    # positive
    with pytest.raises(ValidationError): TestModel(value=1)
    with pytest.raises(ValidationError): TestModel(value="1m")
    with pytest.raises(ValidationError): TestModel(value="1km")
    with pytest.raises(ValidationError): TestModel(value="1cm")

    # zero
    with pytest.raises(ValidationError): TestModel(value=0)
    with pytest.raises(ValidationError): TestModel(value="0m")
    with pytest.raises(ValidationError): TestModel(value="0km")
    with pytest.raises(ValidationError): TestModel(value="0cm")

    # negative
    assert TestModel(value=-1).value == ureg("-1m")
    assert TestModel(value="-1m").value == ureg("-1m")
    assert TestModel(value="-1km").value == ureg("-1km")
    assert TestModel(value="-1cm").value == ureg("-1cm")

def test_quantity_additional_annotations_field_lt():

    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m", strict=False), Field(multiple_of=PydanticPintValue(2, "m", ureg=ureg))]

    # no units
    assert TestModel(value=0).value == ureg("0m")
    assert TestModel(value=2).value == ureg("2m")
    with pytest.raises(ValidationError): TestModel(value=1)

    # meters
    assert TestModel(value="0m").value == ureg("0m")
    assert TestModel(value="2m").value == ureg("2m")
    with pytest.raises(ValidationError): TestModel(value="1m")

    # kilometers
    assert TestModel(value="1km").value == ureg("1km")
    assert TestModel(value="0.5km").value == ureg("0.5km")
    with pytest.raises(ValidationError): TestModel(value="0.001km")

    # centimeters
    with pytest.raises(ValidationError): TestModel(value="1cm")
    with pytest.raises(ValidationError): TestModel(value="2cm")
    assert TestModel(value="200cm").value == ureg("200cm")
