"""Table-driven default values and validation rules for every Config field."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from .level_config import LevelConfig

_DEFAULT_LEVEL_DIM = 21


@dataclass(frozen=True)
class ValidationResult:
    """Holds the validated value and an optional warning message."""

    value: Any
    warning: str | None = None


class BaseValidator(ABC):
    """Abstract base class for all field validators."""

    @abstractmethod
    def validate(self, raw_val: Any, default: Any, field_name: str) -> ValidationResult:
        pass


class IntRangeValidator(BaseValidator):
    """Validates an int is within [min_val, max_val]; resets to default if out of range."""

    def __init__(self, min_val: float = float("-inf"), max_val: float = float("inf")) -> None:
        self.min_val = min_val
        self.max_val = max_val

    def validate(self, raw_val: Any, default: Any, field_name: str) -> ValidationResult:
        if raw_val < self.min_val or raw_val > self.max_val:
            msg = (
                f"'{field_name}' value {raw_val} outside range "
                f"[{self.min_val}..{self.max_val}]. Defaulted to {default}."
            )
            return ValidationResult(default, msg)
        return ValidationResult(raw_val)


class StringValidator(BaseValidator):
    """Validates non-empty string types."""

    def validate(self, raw_val: Any, default: Any, field_name: str) -> ValidationResult:
        if not raw_val.strip():
            msg = f"'{field_name}' must be a non-empty string. Defaulted to '{default}'."
            return ValidationResult(default, msg)
        return ValidationResult(raw_val)


class DimensionValidator(BaseValidator):
    """Validates a maze dimension: falls back to default if out of range, and forces odd numbers."""

    def __init__(self, min_val: int = 9, max_val: int = 51) -> None:
        self.min_val = min_val
        self.max_val = max_val

    def validate(self, raw_val: Any, default: Any, field_name: str) -> ValidationResult:
        if isinstance(raw_val, bool) or not isinstance(raw_val, int):
            val = default
        elif raw_val < self.min_val or raw_val > self.max_val:
            val = default
        else:
            val = raw_val

        # Force odd number
        if val % 2 == 0:
            val = val + 1 if val < self.max_val else val - 1

        if val != raw_val:
            msg = (
                f"'{field_name}' value {raw_val!r} adjusted to {val} "
                f"(odd, range {self.min_val}..{self.max_val})."
            )
            return ValidationResult(val, msg)

        return ValidationResult(val)


class LevelsValidator(BaseValidator):
    """Validates the list of LevelConfig entries and enforces a minimum count."""

    def __init__(self, min_count: int, dim_min: int, dim_max: int, default_dim: int) -> None:
        self.min_count = min_count
        self.default_dim = default_dim
        self.dim_validator = DimensionValidator(dim_min, dim_max)

    def validate(self, raw_val: Any, default: Any, field_name: str) -> ValidationResult:
        if not isinstance(raw_val, list):
            msg = f"'{field_name}' must be a list. Used {len(default)} default levels."
            return ValidationResult(default, msg)

        warnings: list[str] = []
        levels: list[LevelConfig] = []

        for i, item in enumerate(raw_val):
            if not isinstance(item, dict):
                levels.append(LevelConfig(self.default_dim, self.default_dim))
                warnings.append(
                    f"level[{i}] was not an object. Used default "
                    f"{self.default_dim}x{self.default_dim}."
                )
                continue

            w_res = self.dim_validator.validate(item.get("width"), self.default_dim, f"level[{i}].width")
            h_res = self.dim_validator.validate(item.get("height"), self.default_dim, f"level[{i}].height")
            if w_res.warning:
                warnings.append(w_res.warning)
            if h_res.warning:
                warnings.append(h_res.warning)
            levels.append(LevelConfig(w_res.value, h_res.value))

        while len(levels) < self.min_count:
            levels.append(LevelConfig(self.default_dim, self.default_dim))
            warnings.append(
                f"Padded missing level {len(levels)} with default "
                f"{self.default_dim}x{self.default_dim}."
            )

        return ValidationResult(levels, " | ".join(warnings) if warnings else None)


@dataclass(frozen=True)
class FieldSpec:
    """Combines a field's default value, expected type, and validator strategy."""

    default: Any
    expected_type: type
    validator: BaseValidator


class DefaultsSchema:
    """Encapsulates the defaults table and the dict-sanitization process."""

    def __init__(self) -> None:
        default_levels = [LevelConfig(_DEFAULT_LEVEL_DIM, _DEFAULT_LEVEL_DIM) for _ in range(10)]

        self._table: dict[str, FieldSpec] = {
            "highscore_filename": FieldSpec("highscores.json", str, StringValidator()),
            "lives": FieldSpec(3, int, IntRangeValidator(1, 9)),
            "pacgum": FieldSpec(42, int, IntRangeValidator(min_val=1)),
            "levels": FieldSpec(
                default_levels,
                list,
                LevelsValidator(min_count=10, dim_min=9, dim_max=51, default_dim=_DEFAULT_LEVEL_DIM),
            ),
            "points_per_pacgum": FieldSpec(10, int, IntRangeValidator(min_val=0)),
            "points_per_super_pacgum": FieldSpec(50, int, IntRangeValidator(min_val=0)),
            "points_per_ghost": FieldSpec(200, int, IntRangeValidator(min_val=0)),
            "seed": FieldSpec(42, int, IntRangeValidator()),
            "level_max_time": FieldSpec(90, int, IntRangeValidator(10, 600)),
        }

    @staticmethod
    def _type_ok(value: Any, expected: type) -> bool:
        """Checks value against expected, excluding bool from int."""
        if expected is int and isinstance(value, bool):
            return False
        return isinstance(value, expected)

    def sanitize(self, raw_dict: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
        """Validates raw dict input against the schema, returning a clean dict and warnings."""
        clean_dict: dict[str, Any] = {}
        warnings: list[str] = []

        for key, spec in self._table.items():
            if key not in raw_dict:
                clean_dict[key] = spec.default
                warnings.append(f"Missing key '{key}'. Used default {spec.default!r}.")
                continue

            raw_val = raw_dict[key]
            if not self._type_ok(raw_val, spec.expected_type):
                clean_dict[key] = spec.default
                warnings.append(
                    f"'{key}' must be {spec.expected_type.__name__}, "
                    f"got {type(raw_val).__name__}. Defaulted to {spec.default!r}."
                )
                continue

            result = spec.validator.validate(raw_val, spec.default, key)
            clean_dict[key] = result.value
            if result.warning:
                warnings.append(result.warning)

        return clean_dict, warnings