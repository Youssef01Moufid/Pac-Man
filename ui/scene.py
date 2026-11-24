from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from ui.scene_manager import SceneManager


class Scene(ABC):
    """Abstract class that draw the scene """

    def __init__(self, manager: SceneManager) -> None:
        """ Initialize the scene """
        self.manager = manager

    @abstractmethod
    def handle_events(self, event: pygame.event.Event) -> None:
        """ABSTRACT METHOD TO HANDLE EVENTS"""

    @abstractmethod
    def update(self, dt: float) -> None:
        """ABSTRACT METHOD TO UPDATE"""

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """ABSTRACT METHOD TO DRAW"""
