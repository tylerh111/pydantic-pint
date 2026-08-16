from __future__ import annotations

from pint.facets.plain import PlainQuantity
from pydantic import BaseModel

from pydantic_pint import PydanticPintQuantity, get_registry

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


def test_quantity_serialize_default():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[
            PlainQuantity,
            PydanticPintQuantity("m", ser_mode=None, ser_mode_json=None),
        ]

    quantity = TestModel(value="1m")
    assert quantity.model_dump(mode="python")["value"] == ureg("1m")
    assert quantity.model_dump(mode="json")["value"] == str(ureg("1m"))

    quantity = TestModel(value="1.1m")
    assert quantity.model_dump(mode="python")["value"] == ureg("1.1m")
    assert quantity.model_dump(mode="json")["value"] == str(ureg("1.1m"))


def test_quantity_serialize_str():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[
            PlainQuantity,
            PydanticPintQuantity("m", ser_mode="str", ser_mode_json=None),
        ]

    quantity = TestModel(value="1m")
    assert quantity.model_dump(mode="python")["value"] == str(ureg("1m"))
    assert quantity.model_dump(mode="json")["value"] == str(ureg("1m"))

    quantity = TestModel(value="1.1m")
    assert quantity.model_dump(mode="python")["value"] == str(ureg("1.1m"))
    assert quantity.model_dump(mode="json")["value"] == str(ureg("1.1m"))


def test_quantity_serialize_dict():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[
            PlainQuantity,
            PydanticPintQuantity("m", ser_mode="dict", ser_mode_json=None),
        ]

    quantity = TestModel(value="1m")
    assert quantity.model_dump(mode="python")["value"] == {
        "magnitude": ureg("1m").magnitude,
        "units": str(ureg.Unit("meter")),
    }
    assert quantity.model_dump(mode="json")["value"] == {
        "magnitude": ureg("1m").magnitude,
        "units": str(ureg.Unit("meter")),
    }

    quantity = TestModel(value="1.1m")
    assert quantity.model_dump(mode="python")["value"] == {
        "magnitude": ureg("1.1m").magnitude,
        "units": str(ureg.Unit("meter")),
    }
    assert quantity.model_dump(mode="json")["value"] == {
        "magnitude": ureg("1.1m").magnitude,
        "units": str(ureg.Unit("meter")),
    }


def test_quantity_serialize_number():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[
            PlainQuantity,
            PydanticPintQuantity("m", ser_mode="number", ser_mode_json=None),
        ]

    quantity = TestModel(value="1m")
    assert quantity.model_dump(mode="python")["value"] == ureg("1m").magnitude
    assert quantity.model_dump(mode="json")["value"] == ureg("1m").magnitude

    quantity = TestModel(value="1.1m")
    assert quantity.model_dump(mode="python")["value"] == ureg("1.1m").magnitude
    assert quantity.model_dump(mode="json")["value"] == ureg("1.1m").magnitude


def test_quantity_serialize_json_diff_str():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[
            PlainQuantity,
            PydanticPintQuantity("m", ser_mode=None, ser_mode_json="str"),
        ]

    quantity = TestModel(value="1m")
    assert quantity.model_dump(mode="python")["value"] == ureg("1m")
    assert quantity.model_dump(mode="json")["value"] == str(ureg("1m"))

    quantity = TestModel(value="1.1m")
    assert quantity.model_dump(mode="python")["value"] == ureg("1.1m")
    assert quantity.model_dump(mode="json")["value"] == str(ureg("1.1m"))


def test_quantity_serialize_json_diff_dict():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[
            PlainQuantity,
            PydanticPintQuantity("m", ser_mode=None, ser_mode_json="dict"),
        ]

    quantity = TestModel(value="1m")
    assert quantity.model_dump(mode="python")["value"] == ureg("1m")
    assert quantity.model_dump(mode="json")["value"] == {
        "magnitude": ureg("1m").magnitude,
        "units": str(ureg.Unit("meter")),
    }

    quantity = TestModel(value="1.1m")
    assert quantity.model_dump(mode="python")["value"] == ureg("1.1m")
    assert quantity.model_dump(mode="json")["value"] == {
        "magnitude": ureg("1.1m").magnitude,
        "units": str(ureg.Unit("meter")),
    }


def test_quantity_serialize_json_diff_number():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[
            PlainQuantity,
            PydanticPintQuantity("m", ser_mode=None, ser_mode_json="number"),
        ]

    quantity = TestModel(value="1m")
    assert quantity.model_dump(mode="python")["value"] == ureg("1m")
    assert quantity.model_dump(mode="json")["value"] == ureg("1m").magnitude

    quantity = TestModel(value="1.1m")
    assert quantity.model_dump(mode="python")["value"] == ureg("1.1m")
    assert quantity.model_dump(mode="json")["value"] == ureg("1.1m").magnitude
