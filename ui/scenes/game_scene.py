from ui.fake_game import FakeGame
from ui.game_session import GameSession
from ui.hud import Hud
from ui.scene import Scene
from ui.scene_manager import SceneManager
import pygame



class GameScene(Scene):
    def __init__(
            self,
            manager: SceneManager,
            width : int,
            height: int
            ) -> None:
        super().__init__(manager)
        self.game: GameSession = FakeGame()
        self.hud = Hud(self.game)
        self.width = width
        self.height = height

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_p, pygame.K_ESCAPE):
            from ui.scenes.pause_scene import PauseScene
            self.manager.push(PauseScene(self.manager, self.width, self.height))
        self.game.handle_event(event)
    
    def update(self, dt: float) -> None:
        self.game.update(dt)
        if self.game.is_over:
            from ui.scenes.mainmenu_scene import MainMenuScene
            self.manager.replace(MainMenuScene(self.manager, self.width, self.height))
    

    def draw(self, surface: pygame.Surface) -> None:
        self.game.draw(surface)
        self.hud.draw(surface)
