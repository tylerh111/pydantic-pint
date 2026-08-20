from __future__ import annotations

from pint.facets.plain import PlainQuantity
from pydantic import BaseModel

from pydantic_pint import PydanticPintQuantity, get_registry

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


def test_quantity_serialize_unrestricted_nonstrict():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity(strict=False)]

    quantity = TestModel(value="1")
    assert quantity.model_dump(mode="python")["value"] == ureg("1 dimensionless")
    assert quantity.model_dump(mode="json")["value"] == str(ureg("1 dimensionless"))

    quantity = TestModel(value="1m")
    assert quantity.model_dump(mode="python")["value"] == ureg("1m")
    assert quantity.model_dump(mode="json")["value"] == str(ureg("1m"))

    quantity = TestModel(value="1s")
    assert quantity.model_dump(mode="python")["value"] == ureg("1s")
    assert quantity.model_dump(mode="json")["value"] == str(ureg("1s"))


def test_quantity_serialize_unrestricted_strict():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity(strict=True)]

    quantity = TestModel(value="1m")
    assert quantity.model_dump(mode="python")["value"] == ureg("1m")
    assert quantity.model_dump(mode="json")["value"] == str(ureg("1m"))

    quantity = TestModel(value="1s")
    assert quantity.model_dump(mode="python")["value"] == ureg("1s")
    assert quantity.model_dump(mode="json")["value"] == str(ureg("1s"))
