"""Pac-Man "chomping" animation demo.

Run:  python pacman_mouth_demo.py
Arrow keys move Pac-Man. Release the keys and the mouth freezes.
"""
import math

import pygame


class PacmanSprite:
    """Renderer-side visual of Pac-Man.

    Holds only *animation* state (mouth phase). Position, direction and
    whether Pac-Man is moving come from the game model every frame.
    """

    # Angle (degrees, maths convention: 0 = right, counter-clockwise)
    # where the middle of the mouth points for each direction.
    DIRECTION_ANGLES = {"right": 0, "up": 90, "left": 180, "down": 270}

    def __init__(self, radius: int, color=(255, 255, 0),
                 max_mouth_deg: float = 45.0,
                 chomps_per_sec: float = 4.0) -> None:
        self.radius = radius
        self.color = color
        self.max_mouth_deg = max_mouth_deg   # HALF of the full opening
        self.chomps_per_sec = chomps_per_sec
        self._phase = 0.0                    # 0.0 .. 1.0, one full chomp
        self.direction = "right"

    # ---------- animation state ----------
    def update(self, dt: float, direction: str, moving: bool) -> None:
        """Advance the chomp cycle. dt is seconds since last frame."""
        self.direction = direction
        if moving:
            self._phase = (self._phase + dt * self.chomps_per_sec) % 1.0
        # not moving -> phase untouched -> mouth frozen

    def _mouth_half_angle(self) -> float:
        """Triangle wave: phase 0 -> closed, 0.5 -> wide open, 1 -> closed."""
        openness = 1.0 - abs(2.0 * self._phase - 1.0)
        return openness * self.max_mouth_deg

    # ---------- drawing ----------
    def draw(self, surface: pygame.Surface, center: tuple) -> None:
        cx, cy = center
        half = self._mouth_half_angle()

        if half < 1.0:  # mouth (almost) closed: just a full circle
            pygame.draw.circle(surface, self.color,
                               (round(cx), round(cy)), self.radius)
            return

        base = self.DIRECTION_ANGLES[self.direction]
        start = base + half          # upper lip
        end = base + 360 - half      # lower lip, going all the way round

        points = [(cx, cy)]          # the corner of the mouth = centre
        steps = 32
        for i in range(steps + 1):
            a = math.radians(start + (end - start) * i / steps)
            # minus sin: pygame's y axis points DOWN
            points.append((cx + self.radius * math.cos(a),
                           cy - self.radius * math.sin(a)))

        pygame.draw.polygon(surface, self.color, points)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((480, 360))
    pygame.display.set_caption("Pac-Man chomp demo")
    clock = pygame.time.Clock()

    sprite = PacmanSprite(radius=20)
    x, y = 240.0, 180.0
    speed = 120.0  # pixels per second
    direction = "right"

    keys_to_dir = {pygame.K_RIGHT: "right", pygame.K_LEFT: "left",
                   pygame.K_UP: "up", pygame.K_DOWN: "down"}
    velocity = {"right": (1, 0), "left": (-1, 0),
                "up": (0, -1), "down": (0, 1)}

    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # seconds since last frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pressed = pygame.key.get_pressed()
        moving = False
        for key, d in keys_to_dir.items():
            if pressed[key]:
                direction, moving = d, True
                break

        if moving:
            vx, vy = velocity[direction]
            x = max(20, min(460, x + vx * speed * dt))
            y = max(20, min(340, y + vy * speed * dt))

        sprite.update(dt, direction, moving)

        screen.fill((0, 0, 0))
        sprite.draw(screen, (x, y))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
