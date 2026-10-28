"""Retro main menu: title, selectable options, animated chase banner."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import pygame

from app.retro import (BLACK, BLINKY, CLYDE, DOT, INKY, PAC_YELLOW, PINKY,
                       WALL_BLUE, WHITE, RetroFont, Sprites)
from app.scene import Scene, SceneManager


@dataclass
class MenuItem:
    """One line of the menu: its label and what happens on ENTER."""

    label: str
    action: Callable[[], None]


class ChaseBanner:
    """Pac-Man chased by four ghosts across the bottom of the screen.

    Halfway through, the roles flip like in the arcade attract mode:
    the ghosts turn blue and Pac-Man chases them back.
    """

    SPEED = 140.0  # pixels per second

    def __init__(self, width: int, y: int) -> None:
        """Set up the lane the characters run in."""
        self.width: int = width
        self.y: int = y
        self.x: float = -40.0
        self.going_right: bool = True
        self.time: float = 0.0

    def update(self, dt: float) -> None:
        """Move the group and flip direction at the screen edges."""
        self.time += dt
        step = self.SPEED * dt
        self.x += step if self.going_right else -step
        if self.going_right and self.x > self.width + 220:
            self.going_right = False
        elif not self.going_right and self.x < -220:
            self.going_right = True

    def draw(self, surface: pygame.Surface) -> None:
        """Draw Pac-Man plus four ghosts behind or ahead of him."""
        mouth = abs((self.time * 8) % 2 - 1)  # 0 -> 1 -> 0 ping-pong
        wobble = int(self.time * 6) % 2 == 0
        if self.going_right:
            # Ghosts chase Pac-Man to the right.
            Sprites.pacman(surface, (self.x, self.y), 16, mouth, True)
            for i, color in enumerate((BLINKY, PINKY, INKY, CLYDE)):
                gx = self.x - 50 - i * 40
                Sprites.ghost(surface, (gx, self.y - 2), 15, color,
                              True, wobble)
        else:
            # Pac-Man ate a power pellet and chases blue ghosts left.
            for i in range(4):
                gx = self.x - 50 - i * 40
                Sprites.frightened_ghost(surface, (gx, self.y - 2), 15,
                                         wobble)
            Sprites.pacman(surface, (self.x + 40, self.y), 16, mouth, False)


class MainMenuScene(Scene):
    """Main menu required by the subject.

    Options: Start Game, Highscores, Instructions, Exit.
    Navigate with UP/DOWN or W/S, confirm with ENTER or SPACE.
    """

    def __init__(self, manager: SceneManager, font: RetroFont,
                 on_start: Callable[[], None],
                 on_highscores: Callable[[], None],
                 on_instructions: Callable[[], None]) -> None:
        """Build the menu items and the decorative banner.

        The callbacks come from the App, so the menu does not need to
        know how the other scenes are built.
        """
        super().__init__(manager)
        self.font: RetroFont = font
        self.items: list[MenuItem] = [
            MenuItem("START GAME", on_start),
            MenuItem("HIGHSCORES", on_highscores),
            MenuItem("INSTRUCTIONS", on_instructions),
            MenuItem("EXIT", manager.quit),
        ]
        self.selected: int = 0
        self.time: float = 0.0
        self.banner: ChaseBanner | None = None

    # ---- input -----------------------------------------------------
    def handle_event(self, event: pygame.event.Event) -> None:
        """Move the cursor or trigger the selected item."""
        if event.type != pygame.KEYDOWN:
            return
        if event.key in (pygame.K_UP, pygame.K_w):
            self.selected = (self.selected - 1) % len(self.items)
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.selected = (self.selected + 1) % len(self.items)
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER,
                           pygame.K_SPACE):
            self.items[self.selected].action()
        elif event.key == pygame.K_ESCAPE:
            self.manager.quit()

    # ---- logic -----------------------------------------------------
    def update(self, dt: float) -> None:
        """Advance the blink timer and the chase banner."""
        self.time += dt
        if self.banner is not None:
            self.banner.update(dt)

    # ---- drawing ---------------------------------------------------
    def draw(self, surface: pygame.Surface) -> None:
        """Draw frame, title, options, footer and banner."""
        w, h = surface.get_size()
        
        if self.banner is None:
            self.banner = ChaseBanner(w, h - 70)
        surface.fill(BLACK)
        self._draw_frame(surface, w, h)
        self._draw_title(surface, w)
        self._draw_items(surface, w)
        self._draw_footer(surface, w, h)
        self.banner.draw(surface)

    def _draw_frame(self, surface: pygame.Surface, w: int, h: int) -> None:
        """Double blue border like the maze walls."""
        outer = pygame.Rect(12, 12, w - 24, h - 24)
        inner = outer.inflate(-12, -12)
        pygame.draw.rect(surface, WALL_BLUE, outer, 3, border_radius=12)
        pygame.draw.rect(surface, WALL_BLUE, inner, 2, border_radius=8)

    def _blit_center(self, surface: pygame.Surface, img: pygame.Surface,
                     cx: int, y: int) -> None:
        """Blit an image horizontally centred on cx at height y."""
        surface.blit(img, img.get_rect(midtop=(cx, y)))

    def _draw_title(self, surface: pygame.Surface, w: int) -> None:
        """Big yellow title with a drop shadow, plus subtitle."""
        shadow = self.font.render("PAC-MAN", 56, WALL_BLUE)
        title = self.font.render("PAC-MAN", 56, PAC_YELLOW)
        self._blit_center(surface, shadow, w // 2 + 5, 75)
        self._blit_center(surface, title, w // 2, 70)
        sub = self.font.render("GHOSTS!  MORE GHOSTS!", 14, PINKY)
        self._blit_center(surface, sub, w // 2, 150)

    def _draw_items(self, surface: pygame.Surface, w: int) -> None:
        """Options list; the selected one is yellow with Pac-Man beside."""
        top = 230
        gap = 52
        mouth = abs((self.time * 6) % 2 - 1)
        for i, item in enumerate(self.items):
            chosen = i == self.selected
            color = PAC_YELLOW if chosen else WHITE
            img = self.font.render(item.label, 20, color)
            rect = img.get_rect(midtop=(w // 2, top + i * gap))
            surface.blit(img, rect)
            if chosen:
                Sprites.pacman(surface, (rect.left - 30, rect.centery),
                               11, mouth, True)
                # A few dots "to eat" on the right side.
                for d in range(3):
                    pygame.draw.circle(surface, DOT,
                                       (rect.right + 22 + d * 18,
                                        rect.centery), 3)

    def _draw_footer(self, surface: pygame.Surface, w: int, h: int) -> None:
        """Blinking prompt and credits line."""
        if int(self.time * 2) % 2 == 0:
            prompt = self.font.render("PRESS ENTER", 14, WHITE)
            self._blit_center(surface, prompt, w // 2, h - 140)
        credit = self.font.render("42 CURRICULUM  -  2026", 10, INKY)
        self._blit_center(surface, credit, w // 2, h - 36)
