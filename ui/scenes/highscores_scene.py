from typing import Any

import pygame
import os

from ui.highscores import HighScoreManger
from ui.scene import Scene
from config.model import Config

Color = tuple[int, int, int]
FONT_URL = os.path.join('assets', 'fonts', 'PressStart2P-Regular.ttf')

class HighscoresScene(Scene):
    """Shows the top 10 in 3 columns: rank, name, score."""

    BACKGROUND: Color = (0, 0, 0)
    PANEL: Color = (22, 26, 56)
    BORDER: Color = "blue"
    STRIPE: Color = "white"
    TITLE: Color = (255, 215, 0)
    HEADER: Color = "yellow"
    TEXT: Color = (235, 235, 245)
    HINT: Color = "white"
    PODIUM: dict[int, Color] = {
        1: (255, 215, 0),     # gold
        2: (200, 205, 215),   # silver
        3: (205, 127, 50),    # bronze
    }

    def __init__(self, manager: Any, highscores: HighScoreManger, config: Config, width: int, height: int) -> None:
        super().__init__(manager)
        self.highscores = highscores
        try:
            self.title_font = pygame.font.Font(FONT_URL, 42)
        except Exception:
            self.title_font = pygame.font.Font(None, 80)

        try:          
            self.header_font = pygame.font.Font(FONT_URL, 18)
        except Exception:
            self.header_font = pygame.font.Font(None, 30)
        self.row_font = pygame.font.Font(None, 40)
        self.hint_font = pygame.font.Font(None, 28)
        self.config = config
        self.width = width
        self.height = height
    
    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key in (
                pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_BACKSPACE):
            self._back_to_menu()

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        width, height = surface.get_size()
        surface.fill(self.BACKGROUND)

        self._draw_centered(surface, "HIGHSCORES", self.title_font,
                            self.TITLE, width // 2, int(height * 0.12))

        panel = pygame.Rect(0, 0, int(width * 0.6), int(height * 0.68))
        panel.center = (width // 2, int(height * 0.54))
        pygame.draw.rect(surface, self.PANEL, panel, border_radius=16)
        pygame.draw.rect(surface, self.BORDER, panel, width=3,
                         border_radius=16)

        rank_x = panel.left + int(panel.width * 0.10)
        name_x = panel.left + int(panel.width * 0.28)
        score_x = panel.right - int(panel.width * 0.10)
        row_height = panel.height // 12
        top = panel.top + row_height // 2

        self._draw_text(surface, "RANK", self.header_font, self.HEADER,
                        topleft=(rank_x, top))
        self._draw_text(surface, "NAME", self.header_font, self.HEADER,
                        topleft=(name_x, top))
        self._draw_text(surface, "SCORE", self.header_font, self.HEADER,
                        topright=(score_x, top))
        line_y = top + row_height - 8
        pygame.draw.line(surface, self.BORDER, (panel.left + 20, line_y),
                         (panel.right - 20, line_y), 2)

        entries = self.highscores.entries
        if not entries:
            self._draw_centered(surface, "No highscores yet",
                                self.row_font, self.HINT,
                                panel.centerx, panel.centery)
        for rank, (name, score) in enumerate(entries, start=1):
            y = line_y + 10 + (rank - 1) * row_height
            if rank % 2 == 0:
                stripe = pygame.Rect(panel.left + 6, y - 4,
                                     panel.width - 12, row_height)
                pygame.draw.rect(surface, self.STRIPE, stripe,
                                 border_radius=6)
            color = self.PODIUM.get(rank, self.TEXT)
            self._draw_text(surface, f"{rank}.", self.row_font, color,
                            topleft=(rank_x, y))
            self._draw_text(surface, name, self.row_font, color,
                            topleft=(name_x, y))
            self._draw_text(surface, str(score), self.row_font, color,
                            topright=(score_x, y))

        self._draw_centered(surface, "Enter / Esc: Back", self.hint_font,
                            self.HINT, width // 2, int(height * 0.94))

    def _back_to_menu(self) -> None:
        from ui.scenes.mainmenu_scene import MainMenuScene
        self.manager.replace(MainMenuScene(
            self.manager, self.width, self.height, self.config, self.highscores))

    def _draw_text(self, surface: pygame.Surface, text: str,
                   font: pygame.font.Font, color: Color,
                   **anchor: tuple[int, int]) -> None:
        rendered = font.render(text, True, color)
        surface.blit(rendered, rendered.get_rect(**anchor))

    def _draw_centered(self, surface: pygame.Surface, text: str,
                       font: pygame.font.Font, color: Color,
                       x: int, y: int) -> None:
        self._draw_text(surface, text, font, color, center=(x, y))