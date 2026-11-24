from __future__ import annotations

from ui.widgets.widget import Widget
from ui.widgets.button import Button

import pygame


class Menu(Widget):
    """ Menu class holding all buttons make in handle events on click"""
    def __init__(
        self,
        buttons: list[Button],
        center_x: int,
        top_y: int,
        spacing: int = 75,
    ) -> None:

        self.buttons = buttons
        self.selected = 0
        for index, button in enumerate(buttons):
            button.place((center_x, top_y + index * spacing))

    def activate(self) -> None:
        """activate the selected button"""
        self.buttons[self.selected].on_click()

    def _handle_key(self, key: int) -> None:
        """ handle keyboard events in the menu"""
        if key in (pygame.K_UP, pygame.K_w):
            self.selected = (self.selected - 1) % len(self.buttons)
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.selected = (self.selected + 1) % len(self.buttons)
        elif key in (pygame.K_SPACE, pygame.K_RETURN):
            self.activate()

    def _handle_mouse(self, position: tuple[int, int]) -> bool:
        """ handle collidpoint of the mouse with the position """
        for index, button in enumerate(self.buttons):
            if button.rect.collidepoint(position):
                self.selected = index
                return True
        return False

    def handle_event(self, event: pygame.event.Event) -> None:
        """ handle events in the menu if atcivate on click """
        if event.type == pygame.KEYDOWN:
            self._handle_key(event.key)
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._handle_mouse(event.pos):
                self.activate()

    def draw(self, surface: pygame.Surface, selected: bool = False) -> None:
        """ draw the button in the surface """
        for index, button in enumerate(self.buttons):
            button.draw(surface, index == self.selected)
