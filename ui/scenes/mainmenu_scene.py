from ui.scene import Scene
from ui.scene_manager import SceneManager
from ui.widgets.button import Button
from ui.widgets.menu import Menu
from ui.scenes.game_scene import GameScene
from ui.scenes.highscores_scene import HighscoresScene
from ui.highscores import HighScoreManger
from game.gamestate import GameState
from config.model import Config
import pygame

from config.paths import FONT_URL


class MainMenuScene(Scene):
    """"""

    def __init__(
        self,
        manager: SceneManager,
        width: int,
        height: int,
        config: Config,
        highscoremanger: HighScoreManger,
    ) -> None:

        super().__init__(manager)
        self.width = width
        self.height = height
        self.config = config
        self.highscoremanger = highscoremanger
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
        game = GameState(self.config)
        self.manager.replace(
            GameScene(
                self.manager,
                self.width,
                self.height,
                game,
                self.config,
                self.highscoremanger,
            )
        )

    def _instructions(self) -> None:
        from ui.scenes.instrcution_scene import InstructionScene

        self.manager.push(InstructionScene(self.manager, self.config))

    def _high_scores(self) -> None:
        self.manager.replace(
            HighscoresScene(
                self.manager,
                self.highscoremanger,
                self.config,
                self.width,
                self.height,
            )
        )

    def _quit(self) -> None:
        self.manager.quit()

    def handle_events(self, event: pygame.event.Event) -> None:
        self.menu.handle_event(event)

    def update(self, dt: float) -> None:
        """Nothing to update in the menu"""

    def draw_title(self, surface: pygame.Surface) -> None:
        """Draw the title in the menu"""
        w, h = self.font.size("PAC-MAN")
        title = pygame.Rect(0, 0, w, h)

        width_scren = surface.get_width()
        img_blue = self.font.render("PAC-MAN", True, "blue")
        title.midtop = (width_scren // 2 + 5, 245)
        surface.blit(img_blue, title)

        img_yellow = self.font.render("PAC-MAN", True, "yellow")
        title.midtop = (width_scren // 2, 240)
        surface.blit(img_yellow, title)
        try:
            sub_font = pygame.font.Font(FONT_URL, 16)
        except (OSError, FileNotFoundError):
            sub_font = pygame.font.Font(None, 14)
        sub = sub_font.render("GHOSTS!  MORE GHOSTS!", True, (255, 184, 255))
        heigh_screen = surface.get_height()

        surface.blit(
            sub, sub.get_rect(midtop=(width_scren // 2, heigh_screen // 3))
        )

    def draw_frames(self, surface: pygame.Surface) -> None:
        """Draw rectable blue for border"""
        w, h = surface.get_size()
        outter = pygame.Rect(12, 12, w - 24, h - 24)
        inner = outter.inflate(-12, -12)

        pygame.draw.rect(surface, "blue", outter, 3, 14)
        pygame.draw.rect(surface, "blue", inner, 2, 8)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill("black")
        self.draw_frames(surface)
        self.draw_title(surface)
        self.menu.draw(surface)
