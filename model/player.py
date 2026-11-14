"""The player: walks from cell to cell controlled by the keyboard."""

from model.movement import Direction, Movement
from model.entity import Entity

_OPPOSITE: dict[Direction, Direction] = {
    Direction.NORTH: Direction.SOUTH,
    Direction.EAST: Direction.WEST,
    Direction.SOUTH: Direction.NORTH,
    Direction.WEST: Direction.EAST,
}


class Player(Entity):
    """The Pac-Man character controlled by the user."""

    def __init__(self, row: int, col: int, speed: float = 3.0) -> None:
        super().__init__(row, col, speed)

<<<<<<< HEAD
    `position` is the cell it last arrived at. While it travels, `progress`
    (0 to 1) says how far it is toward the next cell in `direction`. It only
    changes direction at a cell center, except for turning back, which is
    allowed at any moment.
    """

    def __init__(
        self,
        position: tuple[int, int],
        speed: float = 3.0,
    ) -> None:
        """Place the player on a cell; speed is in cells per second."""
        self.position = position
        self.direction: Direction | None = None
=======
>>>>>>> 96a23928f223158a0602e23a289d2a763b274575
        self.desired_direction: Direction | None = None

    def set_direction(self, direction: Direction) -> None:
        """Remember the direction the player asked for."""
        self.desired_direction = direction

    def update(
        self,
        dt: float,
        movement: Movement,
        maze: list[list[int]],
    ) -> list[tuple[int, int]]:
        """Check for instant U-turns, then let the parent Entity handle movement."""
        self._turn_back_if_asked(movement, maze)

        return super().update(dt, movement, maze)

    def _choose_direction(
        self,
        movement: Movement,
        maze: list[list[int]],
    ) -> None:
        """At a cell center: take the asked turn, else go on, else stop."""
        desired = self.desired_direction

        if desired is not None and movement.can_move(
            self.row, self.col, maze, desired
        ) is not None:
            self.direction = desired
            self.desired_direction = None
        elif self.direction is not None and movement.can_move(
            self.row, self.col, maze, self.direction
        ) is None:
            self._stop()

    def _turn_back_if_asked(
        self,
        movement: Movement,
        maze: list[list[int]],
    ) -> None:
        """Between two cells, turning back swaps the start and the target."""
        if self.direction is None or self.progress <= 0.0:
            return
        if self.desired_direction != _OPPOSITE[self.direction]:
            return

        target = movement.can_move(
            self.row, self.col, maze, self.direction
        )
        if target is None:
            return

        self.row, self.col = target
        self.direction = self.desired_direction
        self.desired_direction = None
        self.progress = 1.0 - self.progress
<<<<<<< HEAD

    def _stop(self) -> None:
        """Stand still on the current cell."""
        self.direction = None
        self.progress = 0.0

    def get_world_position(self) -> tuple[float, float]:
        """Return the exact (x, y) position: x is the column, y the row."""
        row, col = self.position

        if self.direction is None:
            return float(col), float(row)

        dx, dy = _SCREEN_STEP[self.direction]
        return (
            col + dx * self.progress,
            row + dy * self.progress,
        )
=======
>>>>>>> 96a23928f223158a0602e23a289d2a763b274575
