from dataclasses import dataclass
from .level_config import LevelConfig


@dataclass(frozen=True)
class Config:
    """Fully validated, immutable game configuration."""

    highscore_filename: str
    lives: int
    pacgum: int
    levels: tuple[LevelConfig, ...]
    points_per_pacgum: int
    points_per_super_pacgum: int
    points_per_ghost: int
    seed: int
    level_max_time: int
