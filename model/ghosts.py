
"""Ghost entity with chasing, frightened, and respawning behaviors."""

import random
from enum import Enum, auto

from model.entity import Entity
from model.movement import Direction, Movement
from model.pathfinder import Pathfinder


class GhostState(Enum):
    NORMAL = auto()
    FRIGHTENED = auto()
    EATEN = auto()
    RESPAWNING = auto()


class GhostType(Enum):
    RED = auto()
    PINK = auto()
    CYAN = auto()
    ORANGE = auto()


_OPPOSITE_DIRECTION = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST,
}

_DELTA_DIRECTION = {
    (-1, 0): Direction.NORTH,
    (1, 0): Direction.SOUTH,
    (0, 1): Direction.EAST,
    (0, -1): Direction.WEST,
}


class Ghost(Entity):
    """A ghost with different movement behaviors based on its state."""

    def __init__(
        self,
        row: int,
        col: int,
        speed: float,
        frightened_timer: float,
        respawn_timer: float,
        pathfinder: Pathfinder,
        ghost_type: GhostType
    ) -> None:
        super().__init__(row, col, speed)
        self.base_speed = speed
        self.pathfinder = pathfinder
        self.state = GhostState.NORMAL
        self.frightened_timer = frightened_timer
        self.respawn_timer = respawn_timer
        self.frightened_remaining = 0.0
        self.respawn_remaining = 0.0
        self.target_row = row
        self.target_col = col
        self.ghost_type = ghost_type

    def frightened(self) -> None:
        """Activate frightened mode and restart its countdown."""
        if self.state in (GhostState.NORMAL, GhostState.FRIGHTENED):
            self.state = GhostState.FRIGHTENED
            self.frightened_remaining = self.frightened_timer
            self.speed = self.base_speed * 0.5

    def get_eaten(self) -> None:
        """Mark a frightened ghost as eaten."""
        if self.state == GhostState.FRIGHTENED:
            self.state = GhostState.EATEN
            self.frightened_remaining = 0.0
            self.speed = self.base_speed * 2.0

    def _start_respawning(self) -> None:
        """Start waiting after reaching the original spawn."""
        if self.state != GhostState.EATEN:
            return

        self.state = GhostState.RESPAWNING
        self.respawn_remaining = self.respawn_timer

        self.row = self.spawn_row
        self.col = self.spawn_col
        self.direction = None
        self.progress = 0.0
        self.speed = self.base_speed

    def _update_timers(self, dt: float) -> None:
        """Update frightened and respawning countdowns."""
        if self.state == GhostState.FRIGHTENED:
            self.frightened_remaining = max(
                0.0, self.frightened_remaining - dt
            )

            if self.frightened_remaining <= 0.0:
                self.state = GhostState.NORMAL
                self.speed = self.base_speed

        elif self.state == GhostState.RESPAWNING:
            self.respawn_remaining = max(
                0.0, self.respawn_remaining - dt
            )

            if self.respawn_remaining <= 0.0:
                self.state = GhostState.NORMAL
                self.speed = self.base_speed
                self.direction = None
                self.progress = 0.0

    def set_target(self, target_row: int, target_col: int) -> None:
        """Set the position that the ghost should chase."""
        self.target_row = target_row
        self.target_col = target_col

    @property
    def is_dangerous(self) -> bool:
        """Return whether this ghost can kill Pac-Man."""
        return self.state == GhostState.NORMAL

    @property
    def is_edible(self) -> bool:
        """Return whether Pac-Man can eat this ghost."""
        return self.state == GhostState.FRIGHTENED

    def reset(self) -> None:
        """Restore the ghost to its original state and position."""
        super().reset()

        self.state = GhostState.NORMAL
        self.speed = self.base_speed

        self.frightened_remaining = 0.0
        self.respawn_remaining = 0.0

        self.target_row = self.spawn_row
        self.target_col = self.spawn_col

    def update(
        self,
        dt: float,
        movement: Movement,
        maze: list[list[int]],
    ) -> list[tuple[int, int]]:
        """Update timers, movement, and respawning transitions."""
        self._update_timers(dt)

        if self.state == GhostState.RESPAWNING:
            return []

        if self._has_reached_spawn():
            self._start_respawning()
            return []

        arrived = super().update(dt, movement, maze)

        if self._has_reached_spawn():
            self._start_respawning()

        return arrived

    def _has_reached_spawn(self) -> bool:
        """Check whether an eaten ghost reached its spawn."""
        return (
            self.state == GhostState.EATEN
            and (self.row, self.col)
            == (self.spawn_row, self.spawn_col)
        )

    def _follow_path(
        self,
        maze: list[list[int]],
        goal: tuple[int, int],
    ) -> None:
        """Choose the next direction along a shortest BFS path."""
        path = self.pathfinder.find_path(
            start=(self.row, self.col),
            goal=goal,
            maze=maze,
        )

        if len(path) < 2:
            self.direction = None
            return

        next_row, next_col = path[1]

        delta = (
            next_row - self.row,
            next_col - self.col,
        )

        self.direction = _DELTA_DIRECTION.get(delta)

    def _choose_orange(self, movement: Movement, maze: list[list[int]]) -> None:

        d = abs(self.row - self.target_row) + abs(self.col - self.target_col)

        if d <= 5:
            self._follow_path(maze, (self.target_row, self.target_col))
        else:
            self._choose_random(movement, maze)

    def _choose_random(self, movement: Movement, maze: list[list[int]]) -> None:
        valid_directions: list[Direction] = []

        for direction in Direction:
            if movement.can_move(
                self.row, self.col, maze, direction
            ) is not None:
                valid_directions.append(direction)

        if not valid_directions:
            self.direction = None
            return

        if self.direction is not None:
            opposite = _OPPOSITE_DIRECTION[self.direction]

            alternatives = [
                direction
                for direction in valid_directions
                if direction != opposite
            ]

            if alternatives:
                valid_directions = alternatives

        self.direction = random.choice(valid_directions)

    def _choose_normal(
        self,
        movement: Movement,
        maze: list[list[int]],
    ) -> None:
        """Choose behavior based on ghost type."""

        if self.ghost_type == GhostType.RED:
            self._follow_path(
                maze,
                (self.target_row, self.target_col),
            )

        elif self.ghost_type in (GhostType.PINK, GhostType.CYAN):
            self._choose_random(movement, maze)

        elif self.ghost_type == GhostType.ORANGE:
            self._choose_orange(movement, maze)

    def _choose_eaten(self, maze: list[list[int]]) -> None:
        """Return to the original corner using BFS."""
        self._follow_path(
            maze,
            (self.spawn_row, self.spawn_col),
        )

    def _choose_frightened(
        self,
        movement: Movement,
        maze: list[list[int]],
    ) -> None:
        """Move randomly while avoiding unnecessary reversals."""
        self._choose_random(movement, maze)

    def _choose_direction(
        self,
        movement: Movement,
        maze: list[list[int]],
    ) -> None:
        """Select movement behavior according to the ghost's state."""
        if self.state == GhostState.NORMAL:
            self._choose_normal(movement, maze)

        elif self.state == GhostState.FRIGHTENED:
            self._choose_frightened(movement, maze)

        elif self.state == GhostState.EATEN:
            self._choose_eaten(maze)

        elif self.state == GhostState.RESPAWNING:
            self.direction = None
