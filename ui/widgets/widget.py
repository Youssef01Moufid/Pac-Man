from __future__ import annotations
from abc import ABC, abstractmethod
import pygame


class Widget(ABC):

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        "abstract method to handle inputs"
    

    @abstractmethod
    def draw(self, screen: pygame.Surface, selected: bool = False) -> None:
        "Each widget should be able to draw himself"
