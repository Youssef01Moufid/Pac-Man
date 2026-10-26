from movement import Movement, Direction
from maze.populate import Populate


_OPPOSITE: dict[Direction, Direction] = {
    Direction.NORTH: Direction.SOUTH,
    Direction.EAST: Direction.WEST,
    Direction.SOUTH: Direction.NORTH,
    Direction.WEST: Direction.EAST,
}

class Player:

    def __init__(self, row: int, col: int, speed: float) -> None:

        self.row = row
        self.col = col
        self.speed = speed
        self.direction: Direction = None | None
        self.desired_direction: Direction = None | None
        self.progress = 0.0
        self.spawn = Populate.find_player_spawn()

    def set_direction(self, direction: Direction) -> None:
        self.desired_direction = direction


    def _turn_back(self, movement: Movement, maze: list[list[int]]) -> None:

        if self.direction is None or self.progress <= 0.0:
            return

        if self.desired_direction != _OPPOSITE[self.direction]:
            return

        target = movement.can_move(self.row, self.col, maze, self.direction)
        if target is None:
            return

        self.row, self.col = target
        self.direction = self.desired_direction
        self.desired_direction = None
        self.progress = 1.0 - self.progress