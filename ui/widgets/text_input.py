from ui.widgets.widget import Widget


import pygame


class TextInput(Widget):
    """ Class hand event.Text and add the value typed by the user"""
    def __init__(self) -> None:
        """ Initialize the text input"""
        self.value = ""

    def handle_event(self, event: pygame.event.Event) -> None:
        """ add values if alnume and delete if backspace """
        if event.type == pygame.TEXTINPUT:
            for ch in event.text:
                if ch.isalnum() and len(self.value) < 10:
                    self.value += ch
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            self.value = self.value[:-1]

    def draw(self, screen: pygame.Surface, selected: bool = False) -> None:
        """Nothing this widget to draw"""
