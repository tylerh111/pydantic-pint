# Changes

All notable changes to this project will be documented in this file.

## [Unreleased]

<!-- release notes -->

## [0.6.0] (2026-10-05)

### Added

- Validation now can be configured for unrestricted unit and dimension. By providing no base unit or dimension, e.g. `PydanticPintQuantity()`, any unit and dimension is allowed. Note, the presence of units is still checked for in `strict` mode. ([76](https://github.com/tylerh111/pydantic-pint/issues/76))

### Changed

- Serialization is now split into two parameters: `ser_mode` and `ser_mode_json`. The original behavior is give by `ser_mode_json=None`. Otherwise, `ser_mode_json` overrides `ser_mode` when Pydantic serialization is set to `"json"`, e.g. `quantity.model_dump(mode="json")`.

  Note, this requires a schema update. Serialization schemas are now separate between python vs json serialization. The schema now uses the same typed dictionary schema (i.e. `magnitude` and `unit` dictionary). ([74](https://github.com/tylerh111/pydantic-pint/issues/74))


## [0.5.0] (2026-08-12)

### Fixed

- Fixed issue that caused the serialization schema for `PydanticPintQuantity` from being created.
  This will now allow models that utilize `PydanticPintQuantity` to be used in [FastAPI](https://fastapi.tiangolo.com/) applications. ([57](https://github.com/tylerh111/pydantic-pint/issues/57))
- Fixed issues caused by `pint>=0.25.3`.
  See https://github.com/hgrecco/pint/pull/2260 for more information. ([61](https://github.com/tylerh111/pydantic-pint/issues/61))
- Included the missing serialization return schema in the Pydantic core schema for `PydanticPintQuantity`. ([62](https://github.com/tylerh111/pydantic-pint/issues/62))
- Improved logic for validating units and dimensions when user provides a number as input.
  In this case, the value is forced to be quantity with `dimensionless` units.
  This then can be checked for early on when validating against the specified units / dimensions. ([64](https://github.com/tylerh111/pydantic-pint/issues/64))

### Misc

- [46](https://github.com/tylerh111/pydantic-pint/issues/46), [58](https://github.com/tylerh111/pydantic-pint/issues/58), [59](https://github.com/tylerh111/pydantic-pint/issues/59), [66](https://github.com/tylerh111/pydantic-pint/issues/66), [69](https://github.com/tylerh111/pydantic-pint/issues/69)


## [0.4] (2026-04-09)

### Added

- Add mypy support with `py.typed` and fixed any type hint issues.
  Note, `python==3.8` still has type hint issues due to low mypy version available. ([50](https://github.com/tylerh111/pydantic-pint/issues/50))


## [0.3] (2025-10-26)

### Fixed

- Fixed issue where non-multiplicative units (e.g. degrees Celsius or degrees Fahrenheits) were not being validated correctly. ([44](https://github.com/tylerh111/pydantic-pint/issues/44))
- Fixed issue where dimensions without a default unit cannot be validated. ([47](https://github.com/tylerh111/pydantic-pint/issues/47))


## [0.2] (2025-03-30)

### Added

- Added `"number"` serialization mode to allow users to drop units when serializing a field. ([1](https://github.com/tylerh111/pydantic-pint/issues/1))
- Allow dimensions restriction on fields using `PydanticPintQuantity`.
  Default changed to automatically deduce restrictions instead of only allowing units.
  Using `restriction="units"` forces the restriction to be on units. ([4](https://github.com/tylerh111/pydantic-pint/issues/4))
- Added `exact` option to `PydanticPintQuantity`.
  Enabling this flags forces users to match the exact units of the field. ([11](https://github.com/tylerh111/pydantic-pint/issues/11))
- Added wrapper class for `pint.Quantity` instance to allow value restrictions with `pydantic.Field`.
  Restrictions with `pydantic.Field` and `PydanticPintValue` must be specified as an annotation. ([16](https://github.com/tylerh111/pydantic-pint/issues/16))
- Added unit tests for all advertised features. ([34](https://github.com/tylerh111/pydantic-pint/issues/34))

### Changed

- Changed schema to allow units to be optional when validating a dictionary.
  The check for requiring units happens later in validation by using `strict`. ([29](https://github.com/tylerh111/pydantic-pint/issues/29))

### Fixed

- Fixed issue where `PydanticPintQuantity` fields cannot be used with each other due to different unit registries. ([7](https://github.com/tylerh111/pydantic-pint/issues/7))
- Fixed issue where `PydanticPintValue` did not use global registry. ([18](https://github.com/tylerh111/pydantic-pint/issues/18))
- Refactored validation check on quantity making it simpler to follow.
  The issue regarding strict mode not properly failing validation is fixed as well. ([27](https://github.com/tylerh111/pydantic-pint/issues/27))
- Fixed validation of dimensions when using custom contexts.
  Now, custom contexts that are enabled in the unit registry will be utilized during the check.
  To use the old behavior, enable exact mode which forces the users to provide units of the exact dimensions. ([28](https://github.com/tylerh111/pydantic-pint/issues/28))


## [0.1] (2024-05-06)


### Added

- Added initial code, docs, and tools.

<!-- links -->

[unreleased]: https://github.com/tylerh111/pydantic-pint/compare/0.6.0...main
[0.6.0]: https://github.com/tylerh111/pydantic-pint/releases/tag/0.6.0
[0.5.0]: https://github.com/tylerh111/pydantic-pint/releases/tag/0.5.0
[0.4]: https://github.com/tylerh111/pydantic-pint/releases/tag/0.4
[0.3]: https://github.com/tylerh111/pydantic-pint/releases/tag/0.3
[0.2]: https://github.com/tylerh111/pydantic-pint/releases/tag/0.2
[0.1]: https://github.com/tylerh111/pydantic-pint/releases/tag/0.1
