class IntRangeValidator(BaseValidator):
    """Validates an int is within [min_val, max_val]; resets to default if out of range."""

    def __init__(self, min_val: int | None = None, max_val: int | None = None) -> None:
        self.min_val = min_val
        self.max_val = max_val

    def validate(self, raw_val: Any, default: Any, field_name: str) -> ValidationResult:
        too_low = self.min_val is not None and raw_val < self.min_val
        too_high = self.max_val is not None and raw_val > self.max_val

        if too_low or too_high:
            min_str = self.min_val if self.min_val is not None else "-inf"
            max_str = self.max_val if self.max_val is not None else "inf"

            msg = (
                f"'{field_name}' value {raw_val} outside range "
                f"[{min_str}..{max_str}]. Defaulted to {default}."
            )
            return ValidationResult(default, msg)

        return ValidationResult(raw_val)
