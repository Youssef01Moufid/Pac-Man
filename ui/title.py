import pygame



class TitleDrawer:
    
    def __init__(
            self,
            screen: pygame.Surface
        ):
        self.screen = screen

        self.title_font = pygame.font.Font(None, 48)
        self.title_surf = self.title_font.render("PAC-MAN", True, "gold")

        self.high_scores_fonts = pygame.font.Font(None, 48)
        self.high_scores = self.high_scores_fonts.render("High Score: 0000", True, "white")

        self.current_score_font = pygame.font.Font(None, 48)
        self.current_score = self.current_score_font.render("Score: 0000", True, "white")

        self.times_fonts = pygame.font.Font(None, 48)
        self.times_surf = self.times_fonts.render('Times: 120', True, "white")

        self.lives = 3

    def draw_title(self) -> None:
        """"""
        t_rect = self.title_surf.get_rect(midtop=(self.screen.get_width() // 2, 10))
        t_rect.centery = self.screen.get_height() // 17
        y_rect = self.times_surf.get_rect(midbottom=(self.screen.get_width() // 2, 10))
        y_rect.centery = self.screen.get_height() - 50
        self.screen.blit(self.title_surf, t_rect)
        self.screen.blit(self.times_surf, y_rect)
    
    def draw_scores(self) -> None:
        """"""
        x = self.screen.get_width() - self.high_scores.get_width() - 50
        y = 40
        x_s = self.screen.get_width() - 220
        y_s = self.screen.get_height() - 60
        self.screen.blit(self.high_scores, (x,y))
        self.screen.blit(self.current_score, (x_s, y_s))
    
    def draw_lives(self) -> None:
        """"""
        x = 40
        y = self.screen.get_height() - 80
        img = pygame.image.load('assets/pacman.png').convert_alpha()
        for _ in range(self.lives): 
            img_small = pygame.transform.scale(img, (50, 50))
            self.screen.blit(img_small, (x, y))
            x += 70

    def _draw_frames(self) -> None:
        w, h = self.screen.get_size()

        outer = pygame.Rect(12, 12, w - 24, h - 24)
        inner = outer.inflate(-12, -12)
        pygame.draw.rect(self.screen, 'blue', outer, 3, border_radius=24)
        pygame.draw.rect(self.screen, 'blue', inner, 2, border_radius=24)


    def draw(self):
        self.draw_title()
        self.draw_scores()
        self.draw_lives()
        self._draw_frames()
