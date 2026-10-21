class Populate:

    def __init__(self, maze: list[list[int]], width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.maze = maze

    def _get_OpenCells(self) -> list[tuple[int, int]]:

        open_cells: list[tuple[int, int]] = []

        for i, row in enumerate(self.maze):
            for j, raw in enumerate(self.maze[0]):
                if self.maze[i][j] != 15:
                    open_cells.append((i, j))

        return open_cells

    def _getDist(self, center_w: int, center_h: int) -> dict[tuple[int, int], int]:

        openCells: list[tuple[int, int]] = self._get_OpenCells()
        dists: dict[tuple[int, int], int] = {}

        for i, j in openCells:
            dist = abs(center_h - i) + abs(center_w - j)
            dists[i, j] = dist

        return dists

    def find_player_spawn(self) -> tuple[int, int]:

        center_w = self.width // 2
        center_h = self.height // 2

        dists: dict[tuple[int, int], int] = self._getDist(center_w, center_h)
        playerDim = min(dists, key=dists.get)
        return playerDim

    def find_ghosts_spawn(self) -> list[tuple[int, int]]:

        ghostsDim: list[tuple[int, int]] = []

        ghostsDim.append((0, 0))
        ghostsDim.append((0, self.width - 1))
        ghostsDim.append((self.height - 1, 0))
        ghostsDim.append((self.height - 1, self.width - 1))
        return ghostsDim

    def find_pacgum_spawn(self) -> list[tuple[int, int]]:
        return self._get_OpenCells()

    def find_superpacgum_spawn(self) -> list[tuple[int, int]]:
        return self.find_ghosts_spawn()
