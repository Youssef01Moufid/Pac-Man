from enum import Enum, auto


class Direction(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()


class Movement:

    def _get_target_cell(
        self,
        row: int,
        col: int,
        direction: Direction,
    ) -> tuple[int, int]:

        target_row = row
        target_col = col

        if direction == Direction.NORTH:
            target_row -= 1
        elif direction == Direction.EAST:
            target_col += 1
        elif direction == Direction.SOUTH:
            target_row += 1
        elif direction == Direction.WEST:
            target_col -= 1

        return target_row, target_col

    def can_move(
        self,
        row: int,
        col: int,
        maze: list[list[int]],
        direction: Direction,
    ) -> tuple[int, int] | None:

        if not maze or not maze[0]:
            return None

        rows = len(maze)
        cols = len(maze[0])

        if not (0 <= row < rows and 0 <= col < cols):
            return None

        target_cell = self._get_target_cell(
            row, col, direction
        )

        target_row, target_col = target_cell

        if not (0 <= target_row < rows and 0 <= target_col < cols):
            return None

        wall_bit = {
            Direction.NORTH: 1,
            Direction.EAST: 2,
            Direction.SOUTH: 4,
            Direction.WEST: 8,
        }[direction]

        if maze[row][col] & wall_bit:
            return None

        return target_cell