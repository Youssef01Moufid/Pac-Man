from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from ui.scene_manager import SceneManager


class Scene(ABC):
    """"""
    def __init__(self, manager: SceneManager):
        self.manager = manager
    

    @abstractmethod
    def handle_events(self, event: pygame.event.Event) -> None:
        """"""
 
    @abstractmethod
    def update(self, dt: float) -> None:
        """"""

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """"""
