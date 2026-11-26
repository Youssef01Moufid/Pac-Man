import pygame

from game.gamestate import GameState
from config.paths import FONT_URL


class Hud:
    """ class responsible of the draw the game information """
    HEIGHT = 40
    BG = (20, 20, 40)
    FG = (255, 230, 0)

    def __init__(self, game: GameState) -> None:
        """ Initialization of the game """
        self.game = game
        try:
            self.font = pygame.font.Font(FONT_URL, 28)
        except Exception:
            self.font = pygame.font.Font(None, 28)

    def draw(self, surface: pygame.Surface) -> None:
        """ Draw the game hud in the surface top """
        width = surface.get_width()
        pygame.draw.rect(surface, self.BG, (0, 0, width, self.HEIGHT))

        texts = [
            f"SCORE {self.game.score}",
            f"LIVES {self.game.lives}",
            f"LEVEL {self.game.level_index + 1}",
            f"TIME {int(self.game.time_left)}",
        ]

        slot = width / len(texts)

        for i, text in enumerate(texts):
            img = self.font.render(text, True, self.FG)
            rect = img.get_rect(
                center=(int(slot * i + slot / 2), self.HEIGHT // 2)
            )
            surface.blit(img, rect)
