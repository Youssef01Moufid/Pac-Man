"""Adapter between the external MazeGenerator package and the game's maze."""

import logging
from mazegenerator.mazegenerator import MazeGenerator

logger = logging.getLogger(__name__)

_FALLBACK_RAW: list[list[int]] = [
    [9, 5, 1, 5, 3],
    [10, 9, 0, 3, 10],
    [8, 0, 0, 0, 2],
    [10, 12, 0, 6, 10],
    [12, 5, 4, 5, 6],
]


class MazeAdapter:
    """Converts the external MazeGenerator output into the game's tile grid."""

    def __init__(self, width: int, height: int) -> None:
        """Store the requested maze size, measured in tiles (not cells)."""
        self.width = width
        self.height = height

    def _calculate_cells_dim(self) -> tuple[int, int]:
        """Return (cell_width, cell_height); n cells expand to 2n + 1 tiles."""
        cell_width = (self.width - 1) // 2
        cell_height = (self.height - 1) // 2
        return cell_width, cell_height

    def _run_generator(self, seed: int) -> list[list[int]]:
        """Call the external generator once. May raise any exception."""
        size = self._calculate_cells_dim()
        mazegen = MazeGenerator(size=size, perfect=False, seed=seed)
        return mazegen.maze

    def _is_valid(self, raw: object) -> bool:
        """Check the grid has the expected size and only values 0..15."""
        cell_width, cell_height = self._calculate_cells_dim()
        if not isinstance(raw, list) or len(raw) != cell_height:
            return False
        for row in raw:
            if not isinstance(row, list) or len(row) != cell_width:
                return False
            for value in row:
                if not isinstance(value, int) or not 0 <= value <= 15:
                    return False
        return True

    def _fallback_raw(self) -> list[list[int]]:
        """Return a fresh copy of the fallback, so callers cannot alter it."""
        return [row[:] for row in _FALLBACK_RAW]

    def _generate_raw(self, seed: int) -> list[list[int]]:
        """Return a wall-bit grid, or the fallback maze if generation fails."""
        try:
            raw = self._run_generator(seed)
        except Exception as err:
            logger.warning(
                "Maze generator failed (%s: %s). Using the fallback maze.",
                type(err).__name__,
                err,
            )
            return self._fallback_raw()

        if not self._is_valid(raw):
            logger.warning(
                "Maze generator returned an unexpected grid. "
                "Using the fallback maze."
            )
            return self._fallback_raw()
        return raw
