import random


class Populate:

    def __init__(self, maze: list[list[int]], width: int, height: int, pacgum_count: int) -> None:
        self.width = width
        self.height = height
        self.maze = maze
        self.pacgum_count = pacgum_count

    def _get_OpenCells(self) -> list[tuple[int, int]]:
        """Return all cells that are not completely closed."""
        open_cells: list[tuple[int, int]] = []

        for i, row in enumerate(self.maze):
            for j, raw in enumerate(row):
                if self.maze[i][j] != 15:
                    open_cells.append((i, j))

        return open_cells

    def _getDist(self, center_w: int, center_h: int) -> dict[tuple[int, int], int]:
        """Calculate Manhattan distance to the center."""
        openCells: list[tuple[int, int]] = self._get_OpenCells()
        dists: dict[tuple[int, int], int] = {}

        for i, j in openCells:
            dist = abs(center_h - i) + abs(center_w - j)
            dists[i, j] = dist

        return dists

    def find_player_spawn(self) -> tuple[int, int]:
        """Find the open cell nearest the maze center."""
        center_w = self.width // 2
        center_h = self.height // 2

        dists: dict[tuple[int, int], int] = self._getDist(center_w, center_h)
        playerDim = min(dists, key=dists.get)
        return playerDim

    def find_ghosts_spawn(self) -> list[tuple[int, int]]:
        """Return the four corners of the maze."""
        ghostsDim: list[tuple[int, int]] = []

        ghostsDim.append((0, 0))
        ghostsDim.append((0, self.width - 1))
        ghostsDim.append((self.height - 1, 0))
        ghostsDim.append((self.height - 1, self.width - 1))
        return ghostsDim

    def find_pacgum_spawn(self) -> list[tuple[int, int]]:
        """Place regular Pac-Gums in available cells."""
        available_cells = self._get_OpenCells()

        reserved_cells = {
            self.find_player_spawn(),
            *self.find_ghosts_spawn(),
            *self.find_superpacgum_spawn(),
        }

        available_cells = [
            cell for cell in available_cells
            if cell not in reserved_cells
        ]

        count = min(self.pacgum_count, len(available_cells))

        return random.sample(available_cells, count)

    def find_superpacgum_spawn(self) -> list[tuple[int, int]]:
        """Return Super Pac-Gum positions at the four corners."""
        return self.find_ghosts_spawn()
