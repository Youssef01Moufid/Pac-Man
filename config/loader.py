
"""Load and validate JSON configuration files for the Pac-Man game."""

from pathlib import Path
from typing import Any
import logging
import json

from .defaults import DefaultsSchema
from .model import Config

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Handle reading, parsing, and validating game configuration.

    Read JSON configuration files, remove '#' comments, and validate
    the resulting data using DefaultsSchema.

    If the file is missing, invalid, or cannot be processed, the
    loader attempts to return a Config object with default values.
    """

    def __init__(self, path: str | Path) -> None:
        """Initialize the configuration loader.

        Args:
            path: Path to the JSON configuration file, provided
                as a string or a pathlib.Path object.
        """
        self.path = Path(path)

    def _validate_extension(self) -> bool:
        """Check whether the configuration file has a .json extension.

        The extension comparison is case-insensitive. An invalid
        extension produces a warning and triggers default configuration.

        Returns:
            True if the file extension is .json, otherwise False.
        """
        if self.path.suffix.lower() != ".json":
            logger.warning(
                "Config path '%s' must have a .json extension.",
                "Falling back to defaults.",
                self.path,
            )
            return False
        return True

    def _read_and_strip_comments(self, content: str) -> str:
        """Remove '#' comments while preserving JSON string contents.

        Process the input line by line, removing full-line and inline
        comments introduced by '#' characters outside JSON strings.

        Track quotation marks and escape characters to avoid treating
        '#' characters inside quoted strings as comments.

        Args:
            content: Raw configuration file content.

        Returns:
            Configuration text with comments removed.
        """

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
        """Parse cleaned JSON text into a configuration dictionary.

        Attempt to decode the provided JSON string and verify that
        its root element is a dictionary.

        Log a warning if the JSON syntax is invalid or the root
        element is not an object.

        Args:
            clean_text: JSON configuration text without comments.

        Returns:
            Parsed configuration dictionary if valid.
            An empty dictionary if parsing fails or the root
            element is not a JSON object.
        """
        try:
            data = json.loads(clean_text)
            if isinstance(data, dict):
                return data
            logger.warning(
                "JSON root in '%s' is not an object.",
                "Falling back to defaults.",
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
        """Load and validate the game configuration.

        Check the file extension and existence before reading its
        contents. Remove comments, parse the JSON data, and sanitize
        all configuration fields using DefaultsSchema.

        Log validation warnings and convert the validated levels
        collection into a tuple before constructing Config.

        If an unexpected error occurs, attempt to construct a
        configuration using the schema's default values.

        Returns:
            A Config object containing validated configuration
            values or fallback defaults.
        """
        try:
            if not self._validate_extension():
                raw_dict: dict[str, Any] = {}
            elif not self.path.is_file():
                logger.warning(
                    "Config file '%s' does not exist.",
                    "Falling back to defaults.",
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
                "Unexpected error loading '%s': %s.",
                "Using default configuration.",
                self.path,
                err,
            )
            clean_dict, _ = DefaultsSchema().sanitize({})
            clean_dict["levels"] = tuple(clean_dict["levels"])
            return Config(**clean_dict)
