import pygame
from ui.game_session import GameSession

import os

FONT_URL = os.path.join('assets', 'fonts', 'PressStart2P-Regular.ttf')

class Hud:
    HEIGHT = 40
    BG = (20, 20, 40)
    FG = (255, 230, 0)


    def __init__(self, game: GameSession) -> None:
        self.game = game
        try:
            self.font = pygame.font.Font(FONT_URL, 28)
        except Exception:
            self.font = pygame.font.Font(None, 28)


    def draw(self, surface: pygame.Surface) -> None:
        width = surface.get_width()
        pygame.draw.rect(surface, self.BG, (0, 0, width, self.HEIGHT))


        texts = [
            f"SCORE {self.game.score}",
            f"LIVES {self.game.lives}",
            f"LEVEL {self.game.level}",
            f"TIME {int(self.game.time_left)}"
        ]

        slot = width / len(texts)

        for i, text in enumerate(texts):
            img = self.font.render(text, True, self.FG)
            rect = img.get_rect(center=(int(slot * i + slot / 2), self.HEIGHT // 2))
            surface.blit(img, rect)
