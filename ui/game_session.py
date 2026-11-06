from typing import Protocol
import pygame


class GameSession(Protocol):
    score: int
    lives: int
    level: int
    time_left: float
    is_over: bool

    def handle_event(self, event: pygame.event.Event) -> None: ...
    def update(self, dt: float) -> None: ...
    def draw(self, surface: pygame.Surface) -> None: ...
