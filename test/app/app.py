"""App: owns the window, the clock and the main loop."""

from __future__ import annotations

import pygame

from app.menu import MainMenuScene
from app.placeholder import PlaceholderScene
from app.retro import RetroFont
from app.scene import SceneManager


class App:
    """Creates the window and runs the loop: events -> update -> draw."""

    WIDTH = 720
    HEIGHT = 640
    FPS = 60

    def __init__(self) -> None:
        """Init pygame, the window, shared font and the first scene."""
        pygame.init()
        pygame.display.set_caption("Pac-Man - Ghosts! More ghosts!")
        self.screen: pygame.Surface = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT))
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.font: RetroFont = RetroFont()
        self.manager: SceneManager = SceneManager()
        self.manager.push(self._make_menu())

    def _make_menu(self) -> MainMenuScene:
        """Build the menu and wire each option to a scene."""
        return MainMenuScene(
            self.manager, self.font,
            on_start=lambda: self._open("GAME COMING SOON"),
            on_highscores=lambda: self._open("HIGHSCORES"),
            on_instructions=lambda: self._open("INSTRUCTIONS"),
        )

    def _open(self, title: str) -> None:
        """Push a placeholder until the real scene is written."""
        self.manager.push(PlaceholderScene(self.manager, self.font, title))

    def run(self) -> None:
        """Main loop. Always calls pygame.quit(), even on error."""
        try:
            while self.manager.running:
                dt = self.clock.tick(self.FPS) / 1000.0
                scene = self.manager.current
                if scene is None:
                    break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.manager.quit()
                    else:
                        scene.handle_event(event)
                scene.update(dt)
                scene.draw(self.screen)
                pygame.display.flip()
        finally:
            pygame.quit()


#clone the logic off AI
class APP:

    WIDTH = 720
    HEIGHT = 640
    FPS = 60

    def __init__(
        self):

        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT)
        )
        self.time = pygame.time.Clock()
        self.font = RetroFont()
        self.manager = SceneManager()
        self.manager.push(self._make_menu())
    

    def _make_menu(self):
       
        return MainMenuScene(
                self.manager,
                self.font,
                on_start= lambda : self._open("Gaming on start"),
                on_highscores=lambda: self._open("highescores comming Soon"),
                on_instructions=lambda: self._open("Instractions")
                )
            
    
    def _open(self, title: str):
        self.manager.push(PlaceholderScene(self.manager, self.font, title))
    

    def run(self):

        try:
            while self.manager.running:
                dt = self.time.tick(self.FPS) / 1000.0
                scene = self.manager.current
                if scene is None:
                    break
                
                # 3 steps check events -> update -> draw
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.manager.quit()
                
                    else:
                        scene.handle_event(event)
                scene.update(dt)
                scene.draw(self.screen)
                pygame.display.flip()
        finally:
            pygame.quit()
