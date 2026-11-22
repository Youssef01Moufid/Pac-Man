from ui.widgets.widget import Widget


import pygame

class TextInput(Widget):

    def __init__(self) -> None:
        self.value = ""



    def handle_event(self, event: pygame.event.Event) -> None:
        """ """
        if event.type == pygame.TEXTINPUT:
            for ch in event.text:
                if ch.isalnum() and len(self.value) < 10:
                    self.value += ch
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            self.value = self.value[:-1]

    def draw(self, screen: pygame.Surface, selected: bool = False) -> None:
        """Nothing this widget to draw"""


