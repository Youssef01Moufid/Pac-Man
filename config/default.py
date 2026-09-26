from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class FieldSpec:
    """Defines type checks, default values, and boundary constraints for a single config key."""

    default: Any
    expected_type: type
    validate: Callable[[Any], Any]

    @staticmethod
    def make_int_clamp(min_val: int, max_val: int, default: int) -> Callable[[int], int]:
        def clamp(val: int) -> int:
            if val < min_val or val > max_val:
                return default
            return val
        return clamp

    @staticmethod
    def make_non_empty_string(default: str) -> Callable[[str], str]:
        def check(val: str) -> str:
            if not val.strip():
                return default
            return val
        return check


lives_spec = FieldSpec(
    default=3,
    expected_type=int,
    validate=FieldSpec.make_int_clamp(1, 9, 3),
)

highscore_filename_spec = FieldSpec(
    default="highscores.json",
    expected_type=str,
    validate=FieldSpec.make_non_empty_string("highscores.json"),
)
