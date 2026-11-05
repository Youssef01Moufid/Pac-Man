from model.entity import Entity
from enum import Enum, auto
from model.movement import Movement


class GhostState(Enum):
    NORMAL = auto()
    FRIGHTENED = auto()
    EATEN = auto()
    RESPAWNING = auto()


class Ghost(Entity):

    def __init__(self, row: int, col: int, speed: float, frightened_timer: float, respawn_timer: float) -> None:
        super().__init__(row, col, speed)
        self.based_speed = speed
        self.state = GhostState.NORMAL
        self.frightened_timer = frightened_timer
        self.respawn_timer = respawn_timer
        self.frightened_remaining = 0.0
        self.respawn_remaining = 0.0
        self.target_row = 0
        self.target_col = 0

    def frightened(self) -> None:
        """Activate frightened mode and restart its countdown."""
        if self.state in (GhostState.NORMAL, GhostState.FRIGHTENED):
            self.state = GhostState.FRIGHTENED
            self.frightened_remaining = self.frightened_timer
            self.speed = self.base_speed * 0.5

    def _update_timers(self, dt: float) -> None:
        """Update the ghost's active timers."""

        if self.state == GhostState.FRIGHTENED:
            self.frightened_remaining = max(
                0.0, self.frightened_remaining - dt
            )

            if self.frightened_remaining <= 0.0:
                self.state = GhostState.NORMAL
                self.frightened_remaining = 0.0
                self.speed = self.base_speed

        elif self.state == GhostState.RESPAWNING:
            self.respawn_remaining = max(
                0.0, self.respawn_remaining - dt
            )

            if self.respawn_remaining <= 0.0:
                self.state = GhostState.NORMAL
                self.direction = None
                self.progress = 0.0
                self.speed = self.base_speed

    def get_eaten(self) -> None:
        """Mark the ghost as eaten and prepare it to respawn."""
        if self.state == GhostState.FRIGHTENED:
            self.state = GhostState.EATEN
            self.frightened_remaining = 0.0
            self.speed = self.base_speed * 2.0

    def _start_respawning(self) -> None:
        """Start the respawn countdown and restore the original position."""
        if self.state == GhostState.EATEN:
            self.state = GhostState.RESPAWNING
            self.respawn_remaining = self.respawn_timer
            self.direction = None
            self.progress = 0.0
            self.row = self.spawn_row
            self.col = self.spawn_col

    def set_target(self, target_row: int, target_col: int) -> None:
        """Update the ghost's target (usually the player) before the movement step."""
        self.target_row = target_row
        self.target_col = target_col

    @property
    def is_dangerous(self) -> bool:
        """Returns True if the ghost can kill the player."""
        return self.state == GhostState.NORMAL

    @property
    def is_edible(self) -> bool:
        """Returns True if the ghost can be eaten."""
        return self.state == GhostState.FRIGHTENED

    def update(
        self,
        dt: float,
        movement: Movement,
        maze: list[list[int]]
    ) -> list[tuple[int, int]]:
        """Update ghost timers, check arrivals, and move."""
        self._update_timers(dt)

        if self.state == GhostState.EATEN and self.row == self.spawn_row and self.col == self.spawn_col:
            self._start_respawning()

        if self.state == GhostState.RESPAWNING:
            return []

        return super().update(dt, movement, maze)

    def _choose_direction(self, movement: Movement, maze: list[list[int]]) -> None:

        if self.state == GhostState.NORMAL:
            self._choose_normal(movement, maze)
        elif self.state == GhostState.FRIGHTENED:
            self._choose_frightened(movement, maze)
        elif self.state == GhostState.RESPAWNING:
            self._choose_respawning
