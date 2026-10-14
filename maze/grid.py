from enum import Enum


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
        """Store a tile at (row, col), refusing positions outside the grid."""
        if not self.in_bounds(row, col):
            raise IndexError(
                f"({row}, {col}) is outside the "
                f"{self.height}x{self.width} grid"
            )
        self._tiles[row][col] = tile

    def set_floor(self, row: int, col: int) -> None:
        """Turn the tile at (row, col) into floor.

        Raises:
            IndexError: if (row, col) is outside the grid.
        """
        self._set(row, col, Tile.FLOOR)

    def set_wall(self, row: int, col: int) -> None:
        """Turn the tile at (row, col) into wall.

        Raises:
            IndexError: if (row, col) is outside the grid.
        """
        self._set(row, col, Tile.WALL)

