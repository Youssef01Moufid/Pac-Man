"""Base physical entity for the maze (shared by Player and Ghosts)."""

from model.movement import Direction, Movement

_SCREEN_STEP: dict[Direction, tuple[int, int]] = {
    Direction.NORTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, 1),
    Direction.WEST: (-1, 0),
}


class Entity:
    """A physical character that travels between neighboring cells."""

    def __init__(
        self,
        position: tuple[int, int],
        speed: float,
    ) -> None:
        """Initialize the entity and remember its spawn point for resets."""
        self.position = position
        self.spawn_position = position
        self.direction: Direction | None = None
        self.speed = speed
        self.progress = 0.0

    def reset(self) -> None:
        """Instantly teleport back to the spawn position and stop."""
        self.position = self.spawn_position
        self.direction = None
        self.progress = 0.0

    def update(
        self,
        dt: float,
        movement: Movement,
        maze: list[list[int]],
    ) -> list[tuple[int, int]]:
        """Advance by dt seconds and return the cells arrived at."""
        arrived: list[tuple[int, int]] = []

        if self.direction is None or self.progress <= 0.0:
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
        """Left empty for child classes to fill with their own brains."""
        pass

    def _stop(self) -> None:
        """Stand still on the current cell."""
        self.direction = None
        self.progress = 0.0

    def get_world_position(self) -> tuple[float, float]:
        """Return the exact (x, y) position: x is the column, y the row."""
        row, col = self.position

        if self.direction is None:
            return float(col), float(row)

        d_col, d_row = _SCREEN_STEP[self.direction]
        return (
            col + d_col * self.progress,
            row + d_row * self.progress,
        )