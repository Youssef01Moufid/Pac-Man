"""Instructions screen: controls, rules and cheats (VI.8, VI.5).

Self-contained: every drawing helper lives in this file.
"""

import math
import os
from dataclasses import dataclass

import pygame

from ui.scene import Scene
from ui.scene_manager import SceneManager
from config.model import Config


FONT_URL = os.path.join('assets', 'fonts', 'PressStart2P-Regular.ttf')


class Palette:
    """The original arcade colours."""

    BLACK = (0, 0, 0)
    BLUE = (33, 33, 222)
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)
    PINK = (255, 184, 255)
    CYAN = (0, 255, 255)
    ORANGE = (255, 184, 82)
    WHITE = (255, 255, 255)
    GREY = (80, 80, 80)


@dataclass(frozen=True)
class InstructionPage:
    """One page: a title and (key, description) rows."""

    title: str
    rows: list[tuple[str, str]]
    key_color: tuple[int, int, int] = Palette.YELLOW   # RED for cheat page


class InstructionScene(Scene):
    """Retro-styled controls, rules and cheats."""

    LINE_HEIGHT = 30          # px between two text lines
    ROW_GAP = 14              # extra px between two rows
    COLUMN_GAP = 32           # px between the key and the description

    def __init__(self, manager: SceneManager, config: Config) -> None:
        super().__init__(manager)
        self.pages = self._build_pages(config)
        self.page_index = 0
        self.time = 0.0
        self.font = self._load_font(28)
        self.title_font = self._load_font(30)
        self.small_font = self._load_font(12)


    def _build_pages(self, config: Config) -> list[InstructionPage]:
        """Build the 3 pages. Numbers come from the config, never hardcoded."""
        controls = InstructionPage(
            title="CONTROLS",
            rows=[
                ("ARROWS/WASD", "MOVE"),
                ("P / ESC", "PAUSE / RESUME"),
                ("ENTER", "CHOOSE IN MENUS"),
            ],
        )

        rules = InstructionPage(
            title="RULES",
            rows=[
                ("GOAL", "EAT EVERY PACGUM TO CLEAR THE LEVEL"),
                ("PACGUM", f"+{config.points_per_pacgum} PTS"),
                ("SUPER", f"+{config.points_per_super_pacgum} PTS, "
                          "GHOSTS TURN BLUE AND EDIBLE"),
                ("BLUE GHOST", f"+{config.points_per_ghost} PTS"),
                ("LIVES", f"{config.lives} - A GHOST TOUCH COSTS ONE"),
                ("TIME", f"{config.levels[0].level_max_time} S PER LEVEL, "
                         f"{len(config.levels)} LEVELS"),
            ],
        )

        cheats = InstructionPage(
            title="CHEAT MODE",
            rows=[
                ("F1", "GHOST FREEZE ON / OFF"),
                ("F2", "SPEED BOOST ON / OFF"),
                ("F3", "SKIP TO NEXT LEVEL"),
            ],
            key_color=Palette.RED,
        )

        return [controls, rules, cheats]


    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.manager.pop()
            elif event.key == pygame.K_LEFT:
                self.page_index = (self.page_index - 1) % len(self.pages)
            elif event.key == pygame.K_RIGHT:
                self.page_index = (self.page_index + 1) % len(self.pages)

    def update(self, dt: float) -> None:
        self.time += dt


    def draw(self, surface: pygame.Surface) -> None:
        """Paint the whole screen. Every position is computed from `inner`,
        so the layout follows the window size."""
        width, height = surface.get_size()
        page = self.pages[self.page_index]

        surface.fill(Palette.BLACK)

        inner = self.draw_frames(surface)
        center_x = inner.centerx

        title_rect = self._draw_text(
            surface, self.title_font, page.title, Palette.YELLOW,
            (center_x, inner.top + int(inner.height * 0.08)), "midtop")

        dots_y = inner.bottom - int(inner.height * 0.18)
        hint_y = dots_y + 20
        parade_y = inner.bottom - int(inner.height * 0.07)

        self._draw_rows(surface, page, inner,
                        top=title_rect.bottom + 30, bottom=dots_y - 30)

        # 5. page dots, centred
        self._draw_page_dots(surface, center_x, dots_y)

        # 6. blinking hint: visible half a second, hidden half a second
        if int(self.time * 2) % 2 == 0:
            self._draw_text(surface, self.small_font,
                            "< LEFT  RIGHT >     ESC: MENU", Palette.WHITE,
                            (center_x, hint_y), "midtop")



    def draw_frames(
        self,
        surface: pygame.Surface,
        color: tuple[int, int, int] = Palette.BLUE,
    ) -> pygame.Rect:
        """Two rounded rectangles like the maze walls; returns the inner."""
        w, h = surface.get_size()
        outer = pygame.Rect(12, 12, w - 24, h - 24)
        inner = outer.inflate(-12, -12)          # 6 px smaller on each side
        pygame.draw.rect(surface, color, outer, width=3, border_radius=12)
        pygame.draw.rect(surface, color, inner, width=3, border_radius=12)
        return inner

    def _draw_rows(self, surface: pygame.Surface, page: InstructionPage,
                   inner: pygame.Rect, top: int, bottom: int) -> None:
        """Draw the rows as a two-column table, centred horizontally on the
        screen and vertically between `top` and `bottom`."""

        key_width = max(self.font.size(key)[0] for key, _ in page.rows)


        max_table_width = int(inner.width * 0.85)
        desc_max_width = max_table_width - key_width - self.COLUMN_GAP
        wrapped = [(key, self._wrap_text(desc, desc_max_width))
                   for key, desc in page.rows]

        desc_width = max(self.font.size(line)[0]
                         for _, lines in wrapped for line in lines)
        table_width = key_width + self.COLUMN_GAP + desc_width
        table_height = (sum(len(lines) for _, lines in wrapped)
                        * self.LINE_HEIGHT
                        + (len(wrapped) - 1) * self.ROW_GAP)

        key_x = inner.centerx - table_width // 2
        desc_x = key_x + key_width + self.COLUMN_GAP
        y = top + max(0, (bottom - top - table_height) // 2)

        for key, lines in wrapped:
            self._draw_text(surface, self.font, key, page.key_color,
                            (key_x, y))
            for line in lines:
                self._draw_text(surface, self.font, line, Palette.WHITE,
                                (desc_x, y))
                y += self.LINE_HEIGHT
            y += self.ROW_GAP


    def _load_font(self, size: int) -> pygame.font.Font:
        """Open the pixel font; fall back to pygame's font if it is missing."""
        try:
            return pygame.font.Font(FONT_URL, size)
        except (FileNotFoundError, OSError):
            print(f"Warning: {FONT_URL} not found, using the default font.")
            return pygame.font.Font(None, size * 2)

    def _draw_text(self, surface: pygame.Surface, font: pygame.font.Font,
                   text: str, color: tuple[int, int, int],
                   pos: tuple[int, int], anchor: str = "topleft"
                   ) -> pygame.Rect:
        """Draw one line; `anchor` is the point of the text placed on pos."""
        image = font.render(text, True, color)
        rect = image.get_rect(**{anchor: pos})
        surface.blit(image, rect)
        return rect

    def _wrap_text(self, text: str, max_width: int) -> list[str]:
        """Cut a sentence into lines that each fit in max_width pixels."""
        lines: list[str] = []
        current = ""
        for word in text.split():
            candidate = word if not current else f"{current} {word}"
            if self.font.size(candidate)[0] <= max_width or not current:
                current = candidate
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def _draw_page_dots(self, surface: pygame.Surface, center_x: int,
                        y: int, gap: int = 24) -> None:
        """Big yellow dot for the current page, small grey dots for others."""
        count = len(self.pages)
        start_x = center_x - (count - 1) * gap // 2
        for i in range(count):
            x = start_x + i * gap
            if i == self.page_index:
                pygame.draw.circle(surface, Palette.YELLOW, (x, y), 6)
            else:
                pygame.draw.circle(surface, Palette.GREY, (x, y), 4)


