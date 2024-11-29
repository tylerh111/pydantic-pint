

## Quantity Validation

Models with a `PydanticPintQuantity` annotated field can be constructed from string, dictionaries, or directly with pint quantities.
The `PydanticPintQuantity` enforces a particular unit, but it can convert from any unit of the same quantity.
For instance, `meters` are equivalent to `kilometers` and `watt * second / newton`.

In the example below, all the following are equivalent.

=== "From `str`"

    ```python
    class Model(BaseModel):
        quantity: Annotated[Quantity, PydanticPintQuantity("m")]

    Model(quantity="1000m")
    Model(quantity="1km")
    Model(quantity="1000 W s N^-1")
    ```

=== "From `dict`"

    ```python
    class Model(BaseModel):
        quantity: Annotated[Quantity, PydanticPintQuantity("m")]

    Model(quantity={"magnitude": 1000, "units": "m"})
    Model(quantity={"magnitude": 1, "units": "km"})
    Model(quantity={"magnitude": 1000, "units": "W s N^-1"})
    ```

=== "From `pint.Quantity`"

    ```python
    class Model(BaseModel):
        quantity: Annotated[Quantity, PydanticPintQuantity("m")]

    ureg = UnitRegistry()

    Model(quantity=1000 * ureg.meters)
    Model(quantity=1 * ureg.kilometers)
    Model(quantity=1000 * ureg.watts * ureg.seconds / ureg.newton)
    ```

### Validation Based on Units or Dimensions

The `PydanticPintQuantity` annotation allows for restrictions based on either units or dimensions.
By default, it will try to automatically deduce the restriction type.
To avoid automatic deduction, use `restriction="units"` or `restriction="dimensions"` to be specific.

Restrictions on the unit requires all inputs to the field be convertible to the specified unit.
The value the model stores has the units specified in the annotation.
Restrictions on the dimensions only requires input values to be of the specified dimension.
The units provided (units are required here) are kept.
This means there is no common / default unit for that field.

=== "Restricting Units"

    ```python
    class Model(BaseModel):
        # quantity must be convertible to a "meter" (and will be represented as meters)
        quantity: Annotated[Quantity, PydanticPintQuantity("m")]

    Model(quantity=1 * ureg.meters)
    Model(quantity=1 * ureg.inches)
    #> Model(quantity=<Quantity(1, 'meter')>)
    #> Model(quantity=<Quantity(0.0254, 'meter')>)
    ```

=== "Restricting Dimensions"

    ```python
    class Model(BaseModel):
        # quantity must have units that measure length (and will keep the units provided)
        quantity: Annotated[Quantity, PydanticPintQuantity("[length]")]

    Model(quantity=1 * ureg.meters)
    Model(quantity=1 * ureg.inches)
    #> Model(quantity=<Quantity(1, 'meter')>)
    #> Model(quantity=<Quantity(1, 'inch')>)
    ```

### Strict Mode

By default, strict mode is enabled which forces users to include units when instantiating the model.
Only `str`s, `dict`s, and `pint.Quantity`s can be used to construct the field.
If strict mode is disabled, then users may input a number (i.e. [`numbers.Number`][]), and the serialization will use the units specified in the annotation.

=== "Strict mode enabled (default)"

    ```python
    class Model(BaseModel):
        quantity: Annotated[Quantity, PydanticPintQuantity("m", strict=True)]

    try:
        print(Model(quantity=1))
    except ValidationError as e:
        print(e)
    #> 1 validation error for Model
    #> quantity
    #> Value error, unknown type [type=value_error, input_value='1', input_type=str]
    #>     For further information visit https://errors.pydantic.dev/2.7/v/value_error
    ```

=== "Strict mode disabled"

    ```python
    class Model(BaseModel):
        quantity: Annotated[Quantity, PydanticPintQuantity("m", strict=False)]

    try:
        print(Model(quantity=1))
    except ValidationError as e:
        print(e)
    #> quantity=<Quantity(1, 'meter')>
    ```

### Custom Unit Registry and Unit Registry Context

Developers can pass in a custom `pint.UnitRegistry` or a custom `pint.Context`s.
This feature is useful if there is a pre-existing, custom unit registry already setup.
Custom contexts can be enabled to use different transformation functions between dimensions.
See [pint documentation](https://pint.readthedocs.io/en/latest/user/contexts.html) for more information.

!!! note "Multiple contexts"

    All contexts specified will be added to the unit registry.
    They will all be used in the order specified when converting between two types.

The following example sets up a context that converts between a quantity of length and a quantity of time.


=== "Using a unit registry"

    ```python
    ureg = pint.UnitRegistry()
    ctx = pint.Context()
    ctx.add_transformation("[length]", "[time]", lambda ureg, x: x / (100 * ureg.miles) * (1.5 * ureg.hours))
    ctx.add_transformation("[time]", "[length]", lambda ureg, x: x / (1.5 * ureg.hours) * (100 * ureg.miles))
    ureg.enable_context(ctx)

    class Model(BaseModel):
        quantity: Annotated[Quantity, PydanticPintQuantity("hr", ureg=ureg)]

    print(Model(quantity="100 mi"))
    #> quantity=<Quantity(1.5, 'hour')>
    ```

=== "Using a unit registry context"

    ```python
    ctx = pint.Context()
    ctx.add_transformation("[length]", "[time]", lambda ureg, x: x / (100 * ureg.miles) * (1.5 * ureg.hours))
    ctx.add_transformation("[time]", "[length]", lambda ureg, x: x / (1.5 * ureg.hours) * (100 * ureg.miles))

    class Model(BaseModel):
        quantity: Annotated[Quantity, PydanticPintQuantity("hr", ureg_contexts=[ctx])]

    print(Model(quantity="100 mi"))
    #> quantity=<Quantity(1.5, 'hour')>
    ```

#### Modifying Unit Registry

An interesting side effect with specifying a unit registry is that it can be modified outside the model.
For instance, a developer may set up a unit registry with a particular context enabled, but they can later (programmatically) disable it.
This causes the validation for a model to change.

```python
ureg = pint.UnitRegistry()
ctx = pint.Context()
ctx.add_transformation("[length]", "[time]", lambda ureg, x: x / (100 * ureg.miles) * (1.5 * ureg.hours))
ctx.add_transformation("[time]", "[length]", lambda ureg, x: x / (1.5 * ureg.hours) * (100 * ureg.miles))

class Model(BaseModel):
    quantity: Annotated[Quantity, PydanticPintQuantity("m", ureg=ureg)]

with ureg.context(ctx):
    print(Model(quantity="100 mi"))

try:
    print(Model(quantity="100 mi"))
except ValidationError as e:
    print(e)

#> quantity=<Quantity(1.5, 'hour')>
#> 1 validation error for Model
#> quantity
#>   Value error, Cannot convert from 'mile' ([length]) to 'hour' ([time]) [type=value_error, input_value='100 mi', input_type=str]
#>     For further information visit https://errors.pydantic.dev/2.7/v/value_error
```

!!! warning "Feature or Bug?"

    Whether this is a feature or a bug is up for the developer to decide.
    It is clearly a feature of Pint
    However, Pydantic might consider this behavior a bug due to the validation schema changing over time.

    Consider using unit registry contexts instead.
    They are self contained to the field.

## Quantity Serialization

`PydanticPintQuantity` can be serialized in different ways, similar to the validation.
The annotation can have a serialization mode for `"str"`, `"dict"`, `"number"` or `None` (the default).
The default serialization behavior is to return a `str` or `pint.Quantity`, depending on the whether it produce a JSON serializable object.
That is, it will return a `str` if in Pydantic's `"json"` mode, and it will return a `pint.Quantity` if in Pydantic's `"python"`.
Use `to_json` to change between these modes if using the serialization function directly.

=== "Default (`ser_mode=None`)"

    ```python
    class Model(BaseModel):
        quantity: Annotated[Quantity, PydanticPintQuantity("m")]

    m = Model(quantity={"magnitude": 1000, "units": "m"})

    print(m.model_dump())
    print(m.model_dump(mode="json"))
    #> {'quantity': <Quantity(1000, 'meter')>}
    #> {'quantity': '1000 meter'}
    ```

=== "To `str`"

    ```python
    class Model(BaseModel):
        quantity: Annotated[Quantity, PydanticPintQuantity("m", ser_mode="str")]

    m = Model(quantity={"magnitude": 1000, "units": "m"})

    print(m.model_dump())
    print(m.model_dump(mode="json"))
    #> {'quantity': '1000 meter'}
    #> {'quantity': '1000 meter'}
    ```

=== "To `dict`"

    ```python
    class Model(BaseModel):
        quantity: Annotated[Quantity, PydanticPintQuantity("m", ser_mode="dict")]

    m = Model(quantity={"magnitude": 1000, "units": "m"})

    print(m.model_dump())
    print(m.model_dump(mode="json"))
    #> {'quantity': {'magnitude': 1000, 'units': <Unit('meter')>}}
    #> {'quantity': {'magnitude': 1000, 'units': 'meter'}}
    ```

=== "To `number`"

    ```python
    class Model(BaseModel):
        quantity: Annotated[Quantity, PydanticPintQuantity("m", ser_mode="number")]

    m = Model(quantity={"magnitude": 1000, "units": "m"})

    print(m.model_dump())
    print(m.model_dump(mode="json"))
    #> {'quantity': 1000}
    #> {'quantity': 1000}
    ```

!!! warning "Serializing to a Number"

    Serialization to a number is dangerous due to the loss of information of the units.
    If you need to get the magnitude of the value, it is recommended to use `"dict"` for serialization mode instead.
    Users can pull the magnitude easily from the `"magnitude"` key.
