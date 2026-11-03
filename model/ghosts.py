"""The ghost: an AI entity that chases a target tile through the maze."""

from model.movement import Direction, Movement
from model.entity import Entity

_OPPOSITE: dict[Direction, Direction] = {
    Direction.NORTH: Direction.SOUTH,
    Direction.EAST: Direction.WEST,
    Direction.SOUTH: Direction.NORTH,
    Direction.WEST: Direction.EAST,
}

_TIE_BREAKER_ORDER = [
    Direction.NORTH,
    Direction.EAST,
    Direction.SOUTH,
    Direction.WEST
]


class Ghost(Entity):
    """An AI character that continuously moves toward a target tile."""

    def __init__(self, row: int, col: int, speed: float = 3) -> None:
        super().__init__(row, col, speed)
        self.target_position: tuple[int, int] | None = None

    def update(
        self,
        dt: float,
        movement: Movement,
        maze: list[list[int]],
        target_position: tuple[int, int],  # Passed in from main.py
    ) -> list[tuple[int, int]]:
        """Save the target, then run the parent Entity's math loop."""
        self.target_position = target_position
        return super().update(dt, movement, maze)
    
    def _choose_direction(self, movement: Movement, maze: list[list[int]]) -> None:
