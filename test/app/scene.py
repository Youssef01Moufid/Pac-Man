"""Scene base class and the stack-based SceneManager."""

from __future__ import annotations

from abc import ABC, abstractmethod

import pygame


class Scene(ABC):
    """One screen of the game (menu, playing, pause, ...).

    Every scene gets the same three calls per frame, in this order:
    handle_event (for each pygame event), update, then draw.
    """

    def __init__(self, manager: SceneManager) -> None:
        """Store the manager so the scene can ask for transitions."""
        self.manager: SceneManager = manager

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """React to one input event."""

    @abstractmethod
    def update(self, dt: float) -> None:
        """Advance animations or logic by dt seconds."""

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the scene onto the window surface."""


class SceneManager:
    """Holds a stack of scenes; only the top one receives input.

    push  -> put a scene on top (Pause over Playing).
    pop   -> go back to the scene underneath.
    replace -> swap the top scene (Menu -> Playing).
    """

    def __init__(self) -> None:
        """Start with an empty stack and the app running."""
        self._stack: list[Scene] = []
        self.running: bool = True

    @property
    def current(self) -> Scene | None:
        """Return the top scene, or None when the stack is empty."""
        return self._stack[-1] if self._stack else None

    def push(self, scene: Scene) -> None:
        """Put a scene on top of the stack."""
        self._stack.append(scene)

    def pop(self) -> None:
        """Remove the top scene; quit when nothing is left."""
        if self._stack:
            self._stack.pop()
        if not self._stack:
            self.running = False

    def replace(self, scene: Scene) -> None:
        """Swap the top scene for a new one."""
        if self._stack:
            self._stack.pop()
        self._stack.append(scene)

    def quit(self) -> None:
        """Ask the main loop to stop."""
        self.running = False



#clone for scene

class SCENE(ABC):
    
    def __init__(self, manager: SCENEMANAGER):
        self.manager = manager
    
    @abstractmethod
    def handle_event(self):
        """"""
    
    @abstractmethod
    def update(self):
        """"""
    
    @abstractmethod
    def draw(self):
        """"""


class SCENEMANAGER:

    def __init__(self):
        self.running: bool = True
        self._stack: list[SCENE] = []
    

    @property
    def current(self):
        return self._stack[-1] if self._stack else None

    def push(self, scene: SCENE):
        self._stack.append(scene)
    
    def pop(self):
        if self._stack:
            self._stack.pop()
        self.running = False
    
    def replace(self, scene: SCENE):
        if self._stack:
            self._stack.pop()
        self._stack.append(scene)

    def quit(self):
        self.running = False
