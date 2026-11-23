from ui.scene import Scene
from ui.scene_manager import SceneManager

import pygame




class InstructionScene(Scene):
    """ """
    def __init__(
            self,
            manager: SceneManager,
            ) -> None:
        super().__init__(manager)
        self.manager = manager

    def handle_events(self, event: pygame.event.Event):
        """"""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.pop()

    def update(self, dt: float) -> None:
        """"""


    def _draw_frames(self, surface: pygame.Surface) -> None:
        w, h = surface.get_size()
        outter = pygame.Rect(12, 12, w - 24, h - 24)
        inner = outter.inflate(-12, -12)
        pygame.draw.rect(surface, "blue", outter, width=3, border_radius=14)
        pygame.draw.rect(surface, "blue", inner, width=2, border_radius=8)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((0, 0, 0))
        self._draw_frames(surface)
        