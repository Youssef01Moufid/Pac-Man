from __future__ import annotations


from ui.widgets.widget import Widget
from typing import Callable
import pygame


import os

FONT_PATH = os.path.join('assets', 'fonts', 'PressStart2P-Regular.ttf')


class Button(Widget):

    SIZE_FONT = 36

    def __init__(self, label: str, on_click: Callable[[], None]) -> None:
        """"""
        self.label = label
        self.on_click = on_click
        self.rect = pygame.Rect(0, 0, 0,0)
    
        try:
            self.font = pygame.font.Font(FONT_PATH, self.SIZE_FONT)
        except (FileNotFoundError, OSError):
            self.font = pygame.font.Font(None, self.SIZE_FONT)


    def handle_event(self, event: pygame.event.Event) -> None:
        """Nothing menu widget will handle the on_click"""
    

    def place(self, position: tuple[int, int]) -> None:
        """Each Button should be place into the position"""
        width, height = self.font.size(self.label)
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.midtop = position
    

    def draw(self, screen: pygame.Surface, selected: bool = False) -> None:
        color = "yellow" if selected else "white"
        img = self.font.render(self.label, True, color)
        screen.blit(img, self.rect)
