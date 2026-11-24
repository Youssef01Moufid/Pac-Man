from ui.scene import Scene
from ui.widgets.menu import Menu
from ui.scene_manager import SceneManager
from ui.widgets.button import Button
from ui.highscores import HighScoreManger
from game.gamestate import GameState, GameStatus
from config.model import Config
import pygame


class PauseScene(Scene):
    """ Scene draw on top of the game scene with overlay """
    def __init__(
        self,
        manager: SceneManager,
        width: int,
        height: int,
        game: GameState,
        config: Config,
        highscoremanger: HighScoreManger,
    ):
        """ Initializing the scene with menu buttons """
        super().__init__(manager)
        surface = pygame.display.get_surface()
        self.menu = Menu(
            buttons=[
                Button("Resume", self._resume),
                Button("Back to Menu", self._back_to_menu),
            ],
            center_x=(width // 2),
            top_y=height // 2,
        )
        self.overlay = pygame.Surface(surface.get_size())
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(160)
        self.game = game
        self.config = config
        self.highscoremanger = highscoremanger

    def _resume(self) -> None:
        """ on click pop the scene """
        if self.game.status == GameStatus.PAUSED:
            self.game.resume()
        self.manager.pop()

    def _back_to_menu(self) -> None:
        """ on click return return to the menuscene"""
        from ui.scenes.mainmenu_scene import MainMenuScene

        w, h = self.overlay.get_size()
        self.manager.replace(
            MainMenuScene(
                self.manager, w, h, self.config, self.highscoremanger
            )
        )

    def handle_events(self, event: pygame.event.Event) -> None:
        """ Handle events for the menu scene"""
        if event.type == pygame.KEYDOWN and event.key in (
            pygame.K_p,
            pygame.K_ESCAPE,
        ):
            self._resume()
            return
        self.menu.handle_event(event)

    def update(self, dt: float) -> None:
        """ Nothing to update in the PauseScene"""

    def draw(self, surface: pygame.Surface) -> None:
        """ Copy the surface and draw the menu """
        surface.blit(self.overlay, (0, 0))
        self.menu.draw(surface)
