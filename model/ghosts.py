from model.entity import Entity
from enum import Enum, auto


class GhostState(Enum):
    NORMAL = auto()
    FRIGHTENED = auto()
    EATEN = auto()
    RESPAWNING = auto()


class Ghost(Entity):

    def __init__(self, row: int, col: int, speed: float, frightened_timer: float, respawn_timer: float) -> None:
        super().__init__(row, col, speed)
        self.state = GhostState.NORMAL
        self.frightened_timer = frightened_timer
        self.respawn_timer = respawn_timer
        self.frightened_remaining = 0.0
        self.respawn_remaining = 0.0

    def become_frightened(self) -> None:
        """Activate frightened mode and restart its countdown."""
        self.state = GhostState.FRIGHTENED
        self.frightened_remaining = self.frightened_timer

    def update_timers(self, dt: float) -> None:
        """Update the ghost's active timers."""
        if self.state == GhostState.FRIGHTENED:
            self.frightened_remaining = max(0.0, self.frightened_remaining - dt)

            if self.frightened_remaining <= 0.0:
                self.state = GhostState.NORMAL

