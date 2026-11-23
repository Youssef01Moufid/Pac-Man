"""Table-driven default values and validation rules for Config."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from .level_config import LevelConfig

_DEFAULT_LEVEL_DIM = 21
_DEFAULT_PACGUM = 42
_DEFAULT_LEVEL_TIME = 90


@dataclass(frozen=True)
class ValidationResult:
    """Hold a validated value and an optional warning."""

    value: Any
    warning: str | None = None


class BaseValidator(ABC):
    """Abstract base class for field validators."""

    @abstractmethod
    def validate(
        self,
        raw_val: Any,
        default: Any,
        field_name: str,
    ) -> ValidationResult:
        """Validate a field and return its result."""
        pass


class IntRangeValidator(BaseValidator):
    """Validate an integer within an optional range."""

    def __init__(
        self,
        min_val: int | None = None,
        max_val: int | None = None,
    ) -> None:
        self.min_val = min_val
        self.max_val = max_val

    def validate(
        self,
        raw_val: Any,
        default: Any,
        field_name: str,
    ) -> ValidationResult:
        """Return a valid integer or its default."""
        if type(raw_val) is not int:
            return ValidationResult(
                default,
                f"'{field_name}' must be an integer. "
                f"Defaulted to {default}.",
            )

        too_low = (
            self.min_val is not None
            and raw_val < self.min_val
        )
        too_high = (
            self.max_val is not None
            and raw_val > self.max_val
        )

        if too_low or too_high:
            min_str = (
                self.min_val
                if self.min_val is not None
                else "-inf"
            )
            max_str = (
                self.max_val
                if self.max_val is not None
                else "inf"
            )

            msg = (
                f"'{field_name}' value {raw_val} outside range "
                f"[{min_str}..{max_str}]. "
                f"Defaulted to {default}."
            )
            return ValidationResult(default, msg)

        return ValidationResult(raw_val)


class StringValidator(BaseValidator):
    """Validate non-empty strings."""

    def validate(
        self,
        raw_val: Any,
        default: Any,
        field_name: str,
    ) -> ValidationResult:
        """Return a non-empty string or its default."""
        if not isinstance(raw_val, str) or not raw_val.strip():
            msg = (
                f"'{field_name}' must be a non-empty string. "
                f"Defaulted to '{default}'."
            )
            return ValidationResult(default, msg)

        return ValidationResult(raw_val)


class DimensionValidator(BaseValidator):
    """Validate maze dimensions and enforce odd values."""

    def __init__(
        self,
        min_val: int = 9,
        max_val: int = 51,
    ) -> None:
        self.min_val = min_val
        self.max_val = max_val

    def validate(
        self,
        raw_val: Any,
        default: Any,
        field_name: str,
    ) -> ValidationResult:
        """Return a valid odd maze dimension."""
        if type(raw_val) is not int:
            val = default
        elif raw_val < self.min_val or raw_val > self.max_val:
            val = default
        else:
            val = raw_val

        if val % 2 == 0:
            if val < self.max_val:
                val += 1
            else:
                val -= 1

        if val != raw_val or type(raw_val) is not int:
            msg = (
                f"'{field_name}' value {raw_val!r} "
                f"adjusted to {val} "
                f"(odd, range {self.min_val}..{self.max_val})."
            )
            return ValidationResult(val, msg)

        return ValidationResult(val)


class LevelsValidator(BaseValidator):
    """Validate LevelConfig entries and minimum level count."""

    def __init__(
        self,
        min_count: int,
        dim_min: int,
        dim_max: int,
        default_dim: int,
    ) -> None:
        self.min_count = min_count
        self.default_dim = default_dim

        self.dim_validator = DimensionValidator(
            dim_min, dim_max
        )
        self.pacgum_validator = IntRangeValidator(min_val=0)
        self.time_validator = IntRangeValidator(10, 600)

        self.default_pacgum = _DEFAULT_PACGUM
        self.default_time = _DEFAULT_LEVEL_TIME

    def _default_level(self) -> LevelConfig:
        """Create one level using default values."""
        return LevelConfig(
            width=self.default_dim,
            height=self.default_dim,
            pacgum=self.default_pacgum,
            level_max_time=self.default_time,
        )

    def validate(
        self,
        raw_val: Any,
        default: Any,
        field_name: str,
    ) -> ValidationResult:
        """Validate all levels and add missing default levels."""
        if not isinstance(raw_val, list):
            msg = (
                f"'{field_name}' must be a list. "
                f"Used {len(default)} default levels."
            )
            return ValidationResult(default, msg)

        warnings: list[str] = []
        levels: list[LevelConfig] = []

        for i, item in enumerate(raw_val):
            if not isinstance(item, dict):
                levels.append(self._default_level())
                warnings.append(
                    f"level[{i}] was not an object. "
                    "Used default values."
                )
                continue

            w_res = self.dim_validator.validate(
                item.get("width"),
                self.default_dim,
                f"level[{i}].width",
            )

            h_res = self.dim_validator.validate(
                item.get("height"),
                self.default_dim,
                f"level[{i}].height",
            )

            p_res = self.pacgum_validator.validate(
                item.get("pacgum", self.default_pacgum),
                self.default_pacgum,
                f"level[{i}].pacgum",
            )

            t_res = self.time_validator.validate(
                item.get(
                    "level_max_time",
                    self.default_time,
                ),
                self.default_time,
                f"level[{i}].level_max_time",
            )

            for result in (w_res, h_res, p_res, t_res):
                if result.warning:
                    warnings.append(result.warning)

            levels.append(
                LevelConfig(
                    width=w_res.value,
                    height=h_res.value,
                    pacgum=p_res.value,
                    level_max_time=t_res.value,
                )
            )

        while len(levels) < self.min_count:
            levels.append(self._default_level())
            warnings.append(
                f"Padded missing level {len(levels)} "
                "with default values."
            )

        return ValidationResult(
            levels,
            " | ".join(warnings) if warnings else None,
        )


@dataclass(frozen=True)
class FieldSpec:
    """Combine a default, expected type, and validator."""

    default: Any
    expected_type: type
    validator: BaseValidator


class DefaultsSchema:
    """Manage default configuration and field validation."""

    def __init__(self) -> None:
        default_levels = [
            LevelConfig(
                width=_DEFAULT_LEVEL_DIM,
                height=_DEFAULT_LEVEL_DIM,
                pacgum=_DEFAULT_PACGUM,
                level_max_time=_DEFAULT_LEVEL_TIME,
            )
            for _ in range(10)
        ]

        self._table: dict[str, FieldSpec] = {
            "highscore_filename": FieldSpec(
                "highscores.json",
                str,
                StringValidator(),
            ),
            "lives": FieldSpec(
                3,
                int,
                IntRangeValidator(1, 9),
            ),
            "levels": FieldSpec(
                default_levels,
                list,
                LevelsValidator(
                    min_count=10,
                    dim_min=9,
                    dim_max=51,
                    default_dim=_DEFAULT_LEVEL_DIM,
                ),
            ),
            "points_per_pacgum": FieldSpec(
                10,
                int,
                IntRangeValidator(min_val=0),
            ),
            "points_per_super_pacgum": FieldSpec(
                50,
                int,
                IntRangeValidator(min_val=0),
            ),
            "points_per_ghost": FieldSpec(
                200,
                int,
                IntRangeValidator(min_val=0),
            ),
            "seed": FieldSpec(
                42,
                int,
                IntRangeValidator(),
            ),
        }

    @staticmethod
    def _type_ok(value: Any, expected: type) -> bool:
        """Check a value's type, excluding bool from int."""
        if expected is int:
            return type(value) is int

        return isinstance(value, expected)

    def sanitize(
        self,
        raw_dict: dict[str, Any],
    ) -> tuple[dict[str, Any], list[str]]:
        """Return sanitized configuration and warnings."""
        clean_dict: dict[str, Any] = {}
        warnings: list[str] = []

        for key, spec in self._table.items():
            if key not in raw_dict:
                clean_dict[key] = spec.default
                warnings.append(
                    f"Missing key '{key}'. "
                    f"Used default {spec.default!r}."
                )
                continue

            raw_val = raw_dict[key]

            if not self._type_ok(
                raw_val, spec.expected_type
            ):
                clean_dict[key] = spec.default
                warnings.append(
                    f"'{key}' must be "
                    f"{spec.expected_type.__name__}, "
                    f"got {type(raw_val).__name__}. "
                    f"Defaulted to {spec.default!r}."
                )
                continue

            result = spec.validator.validate(
                raw_val,
                spec.default,
                key,
            )

            clean_dict[key] = result.value

            if result.warning:
                warnings.append(result.warning)

        return clean_dict, warnings
