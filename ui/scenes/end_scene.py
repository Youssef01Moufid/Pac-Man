from ui.scene import Scene
from ui.scene_manager import SceneManager
from config.model import Config
from ui.highscores import HighScoreManger
from ui.widgets.text_input import TextInput
from game.gamestate import GameState
import pygame

import os

FONT_URL = os.path.join("assets", "fonts", "PressStart2P-Regular.ttf")


class EndScene(Scene):

    STYLE = {
        True: ("VICTORY!", "yellow", "YOU CLEARED EVERY LEVEL!"),
        False: ("GAME OVER", "red", "THE GHOSTS GOT YOU."),
    }

    def __init__(
        self,
        manager: SceneManager,
        width: int,
        height: int,
        config: Config,
        highscoremanager: HighScoreManger,
        score: int,
        won: bool,
        game: GameState,
    ) -> None:

        super().__init__(manager)
        self.width = width
        self.height = height
        self.config = config
        self.highscoremanager = highscoremanager
        self.score = score
        self.won = won
        self.game = game
        try:
            self.font_title = pygame.font.Font(FONT_URL, 42)
        except Exception:
            self.font_title = pygame.font.Font(None, 42)
        try:
            self.font_score = pygame.font.Font(FONT_URL, 20)
        except Exception:
            self.font_score = pygame.font.Font(None, 20)
        self.name_input = TextInput()

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            from ui.scenes.highscores_scene import HighscoresScene

            if self.name_input.value:
                self.highscoremanager.add(
                    self.name_input.value, self.game.score
                )
                self.highscoremanager.save()
                self.manager.replace(
                    HighscoresScene(
                        self.manager,
                        self.highscoremanager,
                        self.config,
                        self.width,
                        self.height,
                    )
                )
        self.name_input.handle_event(event)

    def update(self, dt: float) -> None:
        """ """

    def draw_input(self, surface: pygame.Surface) -> None:
        """'ENTER YOUR NAME:' and the box with the typed name."""
        width, height = surface.get_size()

        label = self.font_score.render("ENTER YOUR NAME:", True, "white")
        surface.blit(
            label, label.get_rect(center=(width // 2, int(height * 0.60)))
        )

        box = pygame.Rect(0, 0, int(width * 0.4), int(height * 0.08))
        box.center = (width // 2, int(height * 0.68))
        pygame.draw.rect(surface, "blue", box, width=3, border_radius=8)

        name = self.font_score.render(
            self.name_input.value + "_", True, "yellow"
        )
        surface.blit(name, name.get_rect(center=box.center))

    def draw_frames(self, surface: pygame.Surface) -> None:
        """ """
        w, h = surface.get_size()
        outter = pygame.Rect(12, 12, w - 24, h - 24)
        inner = outter.inflate(-12, -12)
        pygame.draw.rect(surface, "blue", outter, width=4, border_radius=14)
        pygame.draw.rect(surface, "blue", inner, width=3, border_radius=8)

    def draw_title(self, surface: pygame.Surface) -> None:
        """Title in the style colour, with a blue shadow."""
        width, height = surface.get_size()
        title, color, _ = self.STYLE[self.won]
        center = (width // 2, height // 4)

        shadow = self.font_title.render(title, True, "blue")
        surface.blit(
            shadow, shadow.get_rect(center=(center[0] + 5, center[1] + 5))
        )

        text = self.font_title.render(title, True, color)
        surface.blit(text, text.get_rect(center=center))

    def draw_score(self, surface: pygame.Surface) -> None:
        """Message and final score, centred under the title."""
        width, height = surface.get_size()
        _, _, message = self.STYLE[self.won]

        text = self.font_score.render(message, True, "white")
        surface.blit(
            text, text.get_rect(center=(width // 2, int(height * 0.38)))
        )

        score = self.font_score.render(
            f"FINAL SCORE: {self.score}", True, "yellow"
        )
        surface.blit(
            score, score.get_rect(center=(width // 2, int(height * 0.48)))
        )

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill("black")
        self.draw_frames(surface)
        self.draw_title(surface)
        self.draw_score(surface)
        self.draw_input(surface)
