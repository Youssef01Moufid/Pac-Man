from pathlib import Path
from typing import Any
import logging
import json

from .defaults import DefaultsSchema
from .model import Config

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Handles reading, comment stripping, parsing, and schema sanitization for JSON configuration files.

    Guarantees zero crashes: falls back to safe defaults if any file, syntax, or runtime error occurs.
    """

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def _validate_extension(self) -> bool:
        if self.path.suffix.lower() != ".json":
            logger.warning(
                "Config path '%s' must have a .json extension. Falling back to defaults.",
                self.path,
            )
            return False
        return True

    def _read_and_strip_comments(self, content: str) -> str:
        """Strips both full-line and inline '#' comments from the raw text string."""
        cleaned_lines = []

        for line in content.splitlines():
            in_string = False
            escape = False
            comment_index = None

            for i, char in enumerate(line):
                if char == '"' and not escape:
                    in_string = not in_string
                elif char == '#' and not in_string:
                    comment_index = i
                    break

                if char == '\\' and not escape:
                    escape = True
                else:
                    escape = False

            if comment_index is not None:
                line = line[:comment_index]

            cleaned_lines.append(line)

        return "\n".join(cleaned_lines)

    def _parse_json(self, clean_text: str) -> dict[str, Any]:
        try:
            data = json.loads(clean_text)
            if isinstance(data, dict):
                return data
            logger.warning(
                "JSON root in '%s' is not an object. Falling back to defaults.",
                self.path,
            )
        except json.JSONDecodeError as err:
            logger.warning(
                "Invalid JSON syntax in '%s': %s. Falling back to defaults.",
                self.path,
                err,
            )
        return {}

    def load(self) -> Config:
        try:
            if not self._validate_extension():
                raw_dict: dict[str, Any] = {}
            elif not self.path.is_file():
                logger.warning(
                    "Config file '%s' does not exist. Falling back to defaults.",
                    self.path,
                )
                raw_dict = {}
            else:
                raw_text = self.path.read_text(encoding="utf-8")
                clean_text = self._read_and_strip_comments(raw_text)
                raw_dict = self._parse_json(clean_text)

            schema = DefaultsSchema()
            clean_dict, warnings = schema.sanitize(raw_dict)

            for warning in warnings:
                logger.warning("[Config] %s", warning)

            clean_dict["levels"] = tuple(clean_dict["levels"])
            return Config(**clean_dict)

        except Exception as err:
            logger.error(
                "Unexpected error loading '%s': %s. Using default configuration.",
                self.path,
                err,
            )
            clean_dict, _ = DefaultsSchema().sanitize({})
            clean_dict["levels"] = tuple(clean_dict["levels"])
            return Config(**clean_dict)
