from ui.scene import Scene
from ui.widgets.menu import Menu
from ui.scene_manager import SceneManager
from ui.widgets.button import Button

import pygame

class PauseScene(Scene):
    def __init__(
            self,
            manager: SceneManager,
            width: int,
            height: int):
        super().__init__(manager)
        surface = pygame.display.get_surface()
        self.menu = Menu(buttons=[
            Button('Resume', self._resume),
            Button('Back to Menu', self._back_to_menu),
            ],
            center_x=(width // 2),
            top_y=height // 2,
        )
        self.overlay = pygame.Surface(surface.get_size())
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(160)

    def _resume(self) -> None:
        self.manager.pop()
    

    def _back_to_menu(self) -> None:
        from ui.scenes.mainmenu_scene import MainMenuScene
        w, h = self.overlay.get_size()
        self.manager.replace(MainMenuScene(self.manager, w, h))
    

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_p, pygame.K_ESCAPE):
            self._resume()
            return
        self.menu.handle_event(event)
    

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.overlay, (0, 0))
        self.menu.draw(surface)
