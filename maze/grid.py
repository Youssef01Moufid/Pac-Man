"""The maze as the game sees it: a rectangle of wall and floor tiles."""

import logging
from enum import Enum


logger = logging.getLogger(__name__)


class Tile(Enum):
    """The two kinds of square a maze is made of."""

    WALL = 0
    FLOOR = 1


class TileGrid:
    """A rectangle of tiles; positions are (row, col), row first."""

    def __init__(self, width: int, height: int) -> None:
        """Create a grid of the given size, with every tile set to wall."""
        self.width = width
        self.height = height
        self._tiles: list[list[Tile]] = [
            [Tile.WALL for _ in range(width)] for _ in range(height)
        ]

    def in_bounds(self, row: int, col: int) -> bool:
        """Return True if (row, col) lies inside the grid."""
        return 0 <= row < self.height and 0 <= col < self.width

    def is_floor(self, row: int, col: int) -> bool:
        """Return True if (row, col) is inside the grid and is a floor tile."""
        if not self.in_bounds(row, col):
            return False
        return self._tiles[row][col] is Tile.FLOOR

    def _set(self, row: int, col: int, tile: Tile) -> None:
        """Store a tile at (row, col); skip positions outside the grid."""
        if not self.in_bounds(row, col):
            logger.warning(
                "Ignored %s at (%d, %d): outside the %dx%d grid.",
                tile.name,
                row,
                col,
                self.height,
                self.width,
            )
            return
        self._tiles[row][col] = tile

    def set_floor(self, row: int, col: int) -> None:
        """Turn the tile at (row, col) into floor.
        A position outside the grid is ignored and a warning is logged.
        """
        self._set(row, col, Tile.FLOOR)

    def set_wall(self, row: int, col: int) -> None:
        """Turn the tile at (row, col) into wall.
        A position outside the grid is ignored and a warning is logged.
        """
        self._set(row, col, Tile.WALL)

    def get_neighbors(self, row: int, col: int) -> list[tuple[int, int]]:
        """Return the floor tiles directly right, below, above and left.
        Diagonals are not neighbors. Walls and positions outside the grid
        are never returned, so every result is a tile you can stand on.
        """
        neighbors: list[tuple[int, int]] = []

        for d_row, d_col in ((0, 1), (1, 0), (-1, 0), (0, -1)):
            n_row, n_col = row + d_row, col + d_col
            if self.is_floor(n_row, n_col):
                neighbors.append((n_row, n_col))
        return neighbors
