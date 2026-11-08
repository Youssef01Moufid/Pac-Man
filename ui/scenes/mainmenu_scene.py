from ui.scene import Scene
from ui.scene_manager import SceneManager
from ui.widgets.button import Button
from ui.widgets.menu import Menu
from ui.scenes.game_scene import GameScene
import os
import pygame

FONT_URL = os.path.join('assets', 'fonts', 'PressStart2P-Regular.ttf')


class MainMenuScene(Scene):
    """"""
    
    def __init__(
            self,
            manager: SceneManager,
            width: int,
            height: int
            ) -> None:
        
        super().__init__(manager)
        self.width = width
        self.height = height
        
        self.menu = Menu(
            [
                Button("START GAME ", self._start),
                Button("INSTRUCTIONS", self._instructions),
                Button("HIGHSCORES", self._high_scores),
                Button("EXIT", self._quit),
            ],
            center_x=(width // 2),
            top_y=(height // 2),
        )

        try:
            self.font = pygame.font.Font(FONT_URL, 56)
        except (OSError, FileNotFoundError):
            self.font = pygame.font.Font(None, 56)

    def _start(self) -> None:
        self.manager.replace(GameScene(self.manager, self.width, self.height))
    
    def _instructions(self) -> None:
        print("INSTRUCTIONS")
    
    def _high_scores(self) -> None:
        print("HIGHSCORES")

    def _quit(self) -> None:
        self.manager.quit()
    

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._quit()
        else:
            self.menu.handle_event(event)


    def update(self, dt: float):
        """Nothing to update in the menu"""
    

    def draw_title(self, surface: pygame.Surface) -> None:
        """Draw the title in the menu"""
        w, h = self.font.size('PAC-MAN')
        title = pygame.Rect(0, 0, w, h)
        
        width_scren = surface.get_width()
        img_blue = self.font.render('PAC-MAN', True, 'blue')
        title.midtop = (width_scren // 2 + 5, 245)
        surface.blit(img_blue, title)

        img_yellow = self.font.render('PAC-MAN', True, 'yellow')
        title.midtop = (width_scren // 2, 240)
        surface.blit(img_yellow, title)
        try:
            sub_font = pygame.font.Font(FONT_URL, 16)
        except (OSError, FileNotFoundError):
            sub_font = pygame.font.Font(None, 14)
        sub = sub_font.render("GHOSTS!  MORE GHOSTS!", 8, (255, 184, 255))
        heigh_screen = surface.get_height()
        
        surface.blit(sub, sub.get_rect(midtop=(width_scren // 2, heigh_screen // 3)))


    def draw_frames(self, surface: pygame.Surface) -> None:
        """Draw rectable blue for border"""
        w, h = surface.get_size()
        outter = pygame.Rect(12, 12, w - 24, h -24)
        inner = outter.inflate(-12, -12)

        pygame.draw.rect(surface, 'blue', outter, 3, 14)
        pygame.draw.rect(surface, 'blue', inner, 2, 8)
    
    def draw(self, surface: pygame.Surface) -> None:
        surface.fill("black")
        self.draw_frames(surface)
        self.draw_title(surface)
        self.menu.draw(surface)
