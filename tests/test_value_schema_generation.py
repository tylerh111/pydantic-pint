from __future__ import annotations

from pint.facets.plain import PlainQuantity
from pydantic import BaseModel, Field

from pydantic_pint import PydanticPintQuantity, get_registry, pydantic_pint_value

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


def test_quantity_schema_generation_validation():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[
            PlainQuantity,
            PydanticPintQuantity("m", strict=False),
            Field(gt=pydantic_pint_value(0, "m", ureg=ureg)),
        ]

    schema = TestModel.model_json_schema(mode="validation")
    assert isinstance(schema, dict)


def test_quantity_schema_generation_serialization():
    ureg = get_registry()

    class TestModel(BaseModel):
        value: Annotated[
            PlainQuantity,
            PydanticPintQuantity("m", strict=False),
            Field(gt=pydantic_pint_value(0, "m", ureg=ureg)),
        ]

    schema = TestModel.model_json_schema(mode="serialization")
    assert isinstance(schema, dict)
