# Changes

All notable changes to this project will be documented in this file.

## [Unreleased](https://github.com/tylerh111/pydantic-pint/compare/0.0...main)

<!-- release notes -->

## [0.2](https://github.com/tylerh111/pydantic-pint/releases/tag/0.2) - 2025-03-30

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


## [0.1](https://github.com/tylerh111/pydantic-pint/releases/tag/0.1) - 2024-05-06


### Added

- Added initial code, docs, and tools.
