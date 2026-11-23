"""
Module is to load a screen surface and draw into it.
And this using pygame
"""

import pygame
from config.model import Config
from ui.scene_manager import SceneManager
from ui.scenes.mainmenu_scene import MainMenuScene
from ui.highscores import HighScoreManger


class App:

    def __init__(self, config: Config) -> None:
        """"""
        pygame.init()
        self.game = config
        self.manager = SceneManager()
        self.surface = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.highscoremanger = HighScoreManger(config.highscore_filename)
        self.highscoremanger.load()
        self.make_menu(config)

    def make_menu(self, config: Config) -> None:
        """"""
        w, h = self.surface.get_size()
        self.manager.push(
            MainMenuScene(self.manager, w, h, config, self.highscoremanger)
        )

    def run(self) -> None:
        """"""
        try:
            while self.manager.running:
                dt = min(self.clock.tick(60) / 1000.0, 0.05)

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        self.manager.quit()
                        break

                    top = self.manager.top()
                    if top:
                        top.handle_events(event)

                top = self.manager.top()
                if top is None:
                    self.manager.quit()
                else:
                    top.update(dt)
                    self.manager.draw(self.surface)
                pygame.display.flip()

        finally:
            pygame.quit()
