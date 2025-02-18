# Pydantic Pint

[![_](https://img.shields.io/pypi/v/pydantic-pint)](https://pypi.python.org/pypi/pydantic-pint)
[![_](https://img.shields.io/pypi/pyversions/pydantic-pint)](https://github.com/tylerh111/pydantic-pint)
[![_](https://img.shields.io/pypi/l/pydantic-pint)](https://github.com/tylerh111/pydantic-pint/blob/main/LICENSE.md)
[![_](https://img.shields.io/readthedocs/pydantic-pint)](https://pydantic-pint.readthedocs.io)

---

[Pydantic](https://docs.pydantic.dev) is a Python library for data validation and data serialization.
[Pint](https://pint.readthedocs.io) is a Python library for defining, operating, and manipulating physical quantities.
By default, they do not play well with each other.

Many projects that have a need for data validation may also need to work with physical quantities.
[Pydantic Pint](https://pydantic-pint.readthedocs.io) aims to bridge that gap by providing Pydantic validation for Pint quantities.

```python
from pydantic import BaseModel
from pydantic_pint import PydanticPintQuantity
from pint import Quantity
from typing import Annotated

class Box(BaseModel):
    length: Annotated[Quantity, PydanticPintQuantity("m")]
    width: Annotated[Quantity, PydanticPintQuantity("m")]

box = Box(
    length="4m",
    width="2m",
)
```

## Getting Started

### Installation

Pydantic Pint is available as [`pydantic-pint`](https://pypi.python.org/pypi/pydantic-pint) on PyPI.

Pydantic Pint requires both Pydantic and Pint to be installed.
It also requires [`typing.Annotated`](https://docs.python.org/3/library/typing.html#typing.Annotated) (for older version of python use [`typing_extensions`](https://pypi.org/project/typing-extensions/)).

```shell
pip install pydantic-pint
```

### Usage

Pydantic Pint provides `PydanticPintQuantity` which enabled Pydantic validation for Pint quantities.
For a field of a Pydantic model to have quantity validation, it must be annotated with a `PydanticPintQuantity` for a given unit.

```python
from pydantic import BaseModel
from pydantic_pint import PydanticPintQuantity
from pint import Quantity
from typing import Annotated

class Coordinates(BaseModel):
    latitude: Annotated[Quantity, PydanticPintQuantity("deg")]
    longitude: Annotated[Quantity, PydanticPintQuantity("deg")]
    altitude: Annotated[Quantity, PydanticPintQuantity("km")]
```

Users of the model can input anything to the field with a specified unit that is convertible to the units declared in the annotation.
For instance, the units for `Coordinates.altitude` are kilometers, however users can specify meters instead.
`PydanticPintQuantity` will handle the conversion from meters to kilometers.

```python
coord = Coordinates(
    latitude="39.905705 deg",
    longitude="-75.166519 deg",
    altitude="12 meters",
)

print(coord)
#> latitude=<Quantity(39.905705, 'degree')> longitude=<Quantity(-75.166519, 'degree')> altitude=<Quantity(0.012, 'kilometer')>
print(f"{coord!r}")
#> Coordinates(latitude=<Quantity(39.905705, 'degree')>, longitude=<Quantity(-75.166519, 'degree')>, altitude=<Quantity(0.012, 'kilometer')>)
print(coord.model_dump())
#> {'latitude': <Quantity(39.905705, 'degree')>, 'longitude': <Quantity(-75.166519, 'degree')>, 'altitude': <Quantity(0.012, 'kilometer')>}
print(coord.model_dump(mode="json"))
#> {'latitude': '39.905705 degree', 'longitude': '-75.166519 degree', 'altitude': '0.012 kilometer'}
print(f"{coord.model_dump_json()!r}")
#> '{"latitude":"39.905705 degree","longitude":"-75.166519 degree","altitude":"0.012 kilometer"}'
```
