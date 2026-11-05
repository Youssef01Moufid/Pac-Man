from __future__ import annotations

from ui.scene import Scene
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from ui.scene_manager import SceneManager



class TestScene(Scene):

    def __init__(self, manager: SceneManager):
        super().__init__(manager)
    

    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                self.manager.quit()

    def update(self, dt: float) -> None:
        """Nothing to update just drawing scene"""
    


    def draw(self, surface: pygame.Surface):
        """"""
        surface.fill((0, 0, 0))
