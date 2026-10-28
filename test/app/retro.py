"""Retro look: colours, font loading and Pac-Man sprites drawn in code."""

from __future__ import annotations

import math
import os

import pygame

# Arcade palette
BLACK = (0, 0, 0)
WALL_BLUE = (33, 33, 222)
PAC_YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
DOT = (255, 184, 151)
BLINKY = (255, 0, 0)
PINKY = (255, 184, 255)
INKY = (0, 255, 255)
CLYDE = (255, 184, 82)
FRIGHT_BLUE = (33, 33, 255)

FONT_PATH = os.path.join("assets", "fonts", "PressStart2P-Regular.ttf")
print(FONT_PATH)

class RetroFont:
    """Loads the pixel font once, with a safe fallback.

    If assets/fonts/PressStart2P-Regular.ttf is missing, pygame's default
    font is used so the game never crashes because of a missing asset.
    """

    def __init__(self, path: str = FONT_PATH) -> None:
        """Remember where the font file should be."""
        self._path: str = path
        self._cache: dict[int, pygame.font.Font] = {}

    def get(self, size: int) -> pygame.font.Font:
        """Return a font of the given pixel size (cached)."""
        if size not in self._cache:
            try:
                self._cache[size] = pygame.font.Font(self._path, size)
            except (FileNotFoundError, OSError):
                # Default font looks smaller, so scale it up a bit.
                self._cache[size] = pygame.font.Font(None, int(size * 1.6))
        return self._cache[size]

    def render(self, text: str, size: int,
               color: tuple[int, int, int]) -> pygame.Surface:
        """Render text without anti-aliasing for crisp pixel edges."""
        return self.get(size).render(text, False, color)


class Sprites:
    """Draws Pac-Man, ghosts and dots with pygame.draw (no image files)."""

    @staticmethod
    def pacman(surface: pygame.Surface, center: tuple[float, float],
               radius: int, mouth: float, facing_right: bool = True) -> None:
        """Draw Pac-Man as a circle with a wedge cut out.

        Args:
            surface: where to draw.
            center: (x, y) in pixels.
            radius: size in pixels.
            mouth: 0.0 (closed) to 1.0 (wide open).
            facing_right: mouth direction.
        """
        cx, cy = center
        half_angle = math.radians(5 + 40 * mouth)
        base = 0.0 if facing_right else math.pi
        points: list[tuple[float, float]] = [(cx, cy)]
        steps = 24
        start = base + half_angle
        end = base + 2 * math.pi - half_angle
        for i in range(steps + 1):
            a = start + (end - start) * i / steps
            points.append((cx + radius * math.cos(a),
                           cy - radius * math.sin(a)))
        pygame.draw.polygon(surface, PAC_YELLOW, points)

    @staticmethod
    def ghost(surface: pygame.Surface, center: tuple[float, float],
              radius: int, color: tuple[int, int, int],
              look_right: bool = True, wobble: bool = False) -> None:
        """Draw a ghost: round head, straight body, wavy skirt, eyes."""
        cx, cy = center
        r = radius
        pygame.draw.circle(surface, color, (int(cx), int(cy)), r)
        body = pygame.Rect(int(cx - r), int(cy), 2 * r, r)
        pygame.draw.rect(surface, color, body)
        # Skirt: 3 or 4 little triangles, alternating to look animated.
        feet = 4 if wobble else 3
        width = 2 * r / feet
        for i in range(feet):
            x0 = cx - r + i * width
            pygame.draw.polygon(surface, color, [
                (x0, cy + r),
                (x0 + width, cy + r),
                (x0 + width / 2, cy + r + r * 0.4),
            ])
        # Eyes look toward the direction of travel.
        dx = r * 0.15 if look_right else -r * 0.15
        for side in (-1, 1):
            ex = cx + side * r * 0.4
            ey = cy - r * 0.15
            pygame.draw.circle(surface, WHITE, (int(ex), int(ey)),
                               int(r * 0.32))
            pygame.draw.circle(surface, WALL_BLUE, (int(ex + dx), int(ey)),
                               int(r * 0.16))

    @staticmethod
    def frightened_ghost(surface: pygame.Surface,
                         center: tuple[float, float], radius: int,
                         wobble: bool = False) -> None:
        """Draw the blue 'edible' ghost with a wavy mouth."""
        Sprites.ghost(surface, center, radius, FRIGHT_BLUE, wobble=wobble)
        cx, cy = center
        r = radius
        # Cover the normal eyes with small square pale eyes.
        for side in (-1, 1):
            ex = cx + side * r * 0.4
            pygame.draw.circle(surface, FRIGHT_BLUE,
                               (int(ex), int(cy - r * 0.15)), int(r * 0.34))
            pygame.draw.rect(surface, DOT, pygame.Rect(
                int(ex - r * 0.12), int(cy - r * 0.3),
                int(r * 0.24), int(r * 0.24)))
        mouth = [(cx - r * 0.6 + i * r * 0.2,
                  cy + r * 0.35 + (r * 0.12 if i % 2 else -r * 0.12))
                 for i in range(7)]
        pygame.draw.lines(surface, DOT, False, mouth, 2)
