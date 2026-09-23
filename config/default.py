from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class FieldSpec:
    """Defines type checks, default values, and boundary constraints for a single config key."""

    default: Any
    expected_type: type
    validate: Callable[[Any], Any]

    def make_int_clamp(max_val: int, min_val: int) -> Callable:
        def clamp(val: int) -> int:
            if val < min_val:
                return min_val
            if val > max_val:
                return max_val
            return val
        return clamp
