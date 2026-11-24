from __future__ import annotations

from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from ui.scene import Scene


class SceneManager:
    """Managing the scene With stack """

    def __init__(self) -> None:
        """ Initializing the scene manager"""
        self._stack: list[Scene] = []
        self.running: bool = True

    def push(self, scene: Scene) -> None:
        """Push the scene into the stack"""
        self._stack.append(scene)

    def pop(self) -> None:
        """pop scene from stack if no stack end"""
        if self._stack:
            self._stack.pop()
        else:
            self.running = False

    def replace(self, scene: Scene) -> None:
        """
        delete from the stack the old scene and
        append the new scene
        """
        if self._stack:
            self._stack.pop()
        self._stack.append(scene)

    def top(self) -> Scene | None:
        """return the last scene appended"""
        return self._stack[-1] if self._stack else None

    def quit(self) -> None:
        """change the status off the app to false"""
        self.running = False

    def draw(self, surface: pygame.Surface) -> None:
        """draw from the bottom to the top """
        for scene in self._stack:
            scene.draw(surface)
