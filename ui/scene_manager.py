from __future__ import annotations

from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from ui.scene import Scene


class SceneManager:
    """"""

    def __init__(self):
        """"""
        self._stack : list[Scene] = []
        self.running: bool = True

    
    def push(self, scene: Scene) -> None:
        """"""
        self._stack.append(scene)
    

    def pop(self) -> None:
        """"""
        if self._stack:
            self._stack.pop()
        else:
            self.running = False
    

    def replace(self, scene: Scene) -> None:
        """"""
        if self._stack:
            self._stack.pop()
        self._stack.append(scene)
    

    def top(self) -> Scene | None:
        """"""
        return self._stack[-1] if self._stack else None

    def quit(self) -> None:
        """"""
        self.running = False
    
    def draw(self, surface: pygame.Surface) -> None:
        """"""
        for scene in self._stack:
            scene.draw(surface)
            
