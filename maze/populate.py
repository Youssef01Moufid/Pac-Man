from .grid import TileGrid


class Populate:

    def __init__(self, grid: TileGrid) -> None:
        """Chooses where things start inside a maze (spawns, pacgums)."""
        self.grid = grid

    def find_player_spawn(self) -> tuple[int, int]:
        """Keep the grid that will be populated."""
        center_row = self.grid.height // 2
        center_col = self.grid.width // 2
        floor_tiles: list[tuple[int, int]] = []

        for row in range(self.grid.height):
            for col in range(self.grid.width):
                if self.grid.is_floor(row, col):
                    floor_tiles.append((row, col))

        def score(tile: tuple[int, int]) -> tuple[int, int, int]:
            row, col = tile
            distance = abs(row - center_row) + abs(col - center_col)
            return (distance, row, col)

        return min(floor_tiles, key=score)

    def find_ghosts_spawn(self) -> list[tuple[int, int]]:
        """Find up to four distinct floor tiles near the corners."""
        candidates = [
            (1, 1),
            (1, self.grid.width - 2),
            (self.grid.height - 2, 1),
            (self.grid.height - 2, self.grid.width - 2),
        ]

        player_spawn = self.find_player_spawn()
        ghosts_spawn: list[tuple[int, int]] = []

        for row, col in candidates:
            position = (row, col)

            if (
                self.grid.is_floor(row, col)
                and position != player_spawn
                and position not in ghosts_spawn
            ):
                ghosts_spawn.append(position)

        return ghosts_spawn

    def find_pacgum_spawn(self) -> list[tuple[int, int]]:
        """Find floor tiles not reserved for Pac-Man or ghosts."""
        occupied = {
            self.find_player_spawn(),
            *self.find_ghosts_spawn(),
        }

        pacgum_spawn: list[tuple[int, int]] = []

        for row in range(self.grid.height):
            for col in range(self.grid.width):
                position = (row, col)

                if self.grid.is_floor(row, col) and position not in occupied:
                    pacgum_spawn.append(position)

        return pacgum_spawn
