
"""Represent a maze and its remaining collectibles."""

from enum import Enum, auto


class CollectibleType(Enum):
    """Types of collectibles in the maze."""

    NONE = auto()
    PACGUM = auto()
    SUPER_PACGUM = auto()


class Level:
    """Manage the maze and its remaining Pac-Gums."""

    def __init__(
        self,
        maze: list[list[int]],
        pacgums: set[tuple[int, int]],
        super_pacgums: set[tuple[int, int]],
    ) -> None:
        """Initialize the level with its maze and collectibles."""
        self.maze = maze
        self.pacgums = pacgums.copy()
        self.super_pacgums = super_pacgums.copy()

    def eat_at(self, position: tuple[int, int]) -> CollectibleType:
        """Remove and return the collectible at a position."""
        if position in self.super_pacgums:
            self.super_pacgums.remove(position)
            return CollectibleType.SUPER_PACGUM

        if position in self.pacgums:
            self.pacgums.remove(position)
            return CollectibleType.PACGUM

        return CollectibleType.NONE

    def is_complete(self) -> bool:
        """Return True when all regular Pac-Gums are eaten."""
        return not self.pacgums and not self.super_pacgums
