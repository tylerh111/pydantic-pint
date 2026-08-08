from __future__ import annotations

from pint.facets.plain import PlainQuantity
from pydantic import BaseModel

from pydantic_pint import PydanticPintQuantity

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


def test_quantity_schema_generation_validation():

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m")]

    schema = TestModel.model_json_schema(mode="validation")
    assert isinstance(schema, dict)


def test_quantity_schema_generation_serialization():

    class TestModel(BaseModel):
        value: Annotated[PlainQuantity, PydanticPintQuantity("m")]

    schema = TestModel.model_json_schema(mode="serialization")
    assert isinstance(schema, dict)
