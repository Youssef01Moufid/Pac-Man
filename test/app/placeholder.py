"""Temporary screen used until the real scene exists."""

from __future__ import annotations

import pygame

from app.retro import BLACK, PAC_YELLOW, WHITE, RetroFont
from app.scene import Scene, SceneManager


class PlaceholderScene(Scene):
    """Shows a title and 'ESC TO GO BACK'; pops itself on Escape."""

    def __init__(self, manager: SceneManager, font: RetroFont,
                 title: str) -> None:
        """Remember which screen this stands in for."""
        super().__init__(manager)
        self.font: RetroFont = font
        self.title: str = title

    def handle_event(self, event: pygame.event.Event) -> None:
        """Escape returns to the menu underneath."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.pop()

    def update(self, dt: float) -> None:
        """Nothing to animate."""

    def draw(self, surface: pygame.Surface) -> None:
        """Title and hint, centred."""
        w, h = surface.get_size()
        surface.fill(BLACK)
        title = self.font.render(self.title, 24, PAC_YELLOW)
        hint = self.font.render("ESC TO GO BACK", 12, WHITE)
        surface.blit(title, title.get_rect(center=(w // 2, h // 2 - 20)))
        surface.blit(hint, hint.get_rect(center=(w // 2, h // 2 + 30)))
