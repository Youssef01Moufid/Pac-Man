from dataclasses import dataclass


@dataclass(frozen=True)
class LevelConfig:
    """A single level's maze dimensions."""

    width: int
    height: int
