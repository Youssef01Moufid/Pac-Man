"""The player: walks from cell to cell along the corridors of the maze."""

from model.movement import Direction, Movement

_OPPOSITE: dict[Direction, Direction] = {
    Direction.NORTH: Direction.SOUTH,
    Direction.EAST: Direction.WEST,
    Direction.SOUTH: Direction.NORTH,
    Direction.WEST: Direction.EAST,
}

_SCREEN_STEP: dict[Direction, tuple[int, int]] = {
    Direction.NORTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, 1),
    Direction.WEST: (-1, 0),
}


class Player:
    """A character that travels between neighboring cells at a set speed.

    `position` is the cell it last arrived at. While it travels, `progress`
    (0 to 1) says how far it is toward the next cell in `direction`. It only
    changes direction at a cell center, except for turning back, which is
    allowed at any moment.
    """

    def __init__(
        self,
        position: tuple[int, int],
        speed: float = 5.0,
    ) -> None:
        """Place the player on a cell; speed is in cells per second."""
        self.position = position
        self.direction: Direction | None = None
        self.desired_direction: Direction | None = None
        self.speed = speed
        self.progress = 0.0

    def set_direction(self, direction: Direction) -> None:
        """Remember the direction the player asked for."""
        self.desired_direction = direction

    def update(
        self,
        dt: float,
        movement: Movement,
        maze: list[list[int]],
    ) -> list[tuple[int, int]]:
        """Advance by dt seconds and return the cells arrived at.

        Usually the list has zero or one cell. A very slow frame can cross
        several cells, and each one is reported so none is skipped.
        """
        arrived: list[tuple[int, int]] = []

        self._turn_back_if_asked(movement, maze)
        if self.direction is None:
            self._choose_direction(movement, maze)
            if self.direction is None:
                return arrived

        self.progress += self.speed * dt

        while self.direction is not None and self.progress >= 1.0:
            target = movement.can_move(
                self.position[0], self.position[1], maze, self.direction
            )
            if target is None:
                self._stop()
                break
            self.position = target
            self.progress -= 1.0
            arrived.append(target)
            self._choose_direction(movement, maze)

        return arrived

    def _choose_direction(
        self,
        movement: Movement,
        maze: list[list[int]],
    ) -> None:
        """At a cell center: take the asked turn, else go on, else stop."""
        row, col = self.position
        desired = self.desired_direction

        if desired is not None and movement.can_move(
            row, col, maze, desired
        ) is not None:
            self.direction = desired
            self.desired_direction = None
        elif self.direction is not None and movement.can_move(
            row, col, maze, self.direction
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
            self.position[0], self.position[1], maze, self.direction
        )
        if target is None:
            return

        self.position = target
        self.direction = self.desired_direction
        self.desired_direction = None
        self.progress = 1.0 - self.progress

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