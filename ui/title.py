import pygame



class TitleDrawer:
    
    def __init__(
            self,
            screen: pygame.Surface
        ):
        self.screen = screen
        self.title_font = pygame.font.Font(None, 48)
        self.high_scores_fonts = pygame.font.Font(None, 48)
        self.lives_fonts = pygame.font.Font(None, 48)
        self.current_score_font = pygame.font.Font(None, 48)
        self.title_surf = self.title_font.render("PAC-MAN", True, "gold")
        self.high_scores = self.high_scores_fonts.render("High Score: 0000", True, "white")
        self.current_score = self.current_score_font.render("Score: 0000", True, "white")
        self.lives = 3

    def draw_title(self) -> None:

        t_rect = self.title_surf.get_rect(midtop=(self.screen.get_width() // 2, 10))
        t_rect.centery = self.screen.get_height() // 17
        self.screen.blit(self.title_surf, t_rect)

    
    def draw_scores(self) -> None:
        x = self.screen.get_width() - self.high_scores.get_width() - 20
        y = 20
        x_s = self.screen.get_width() - 200
        y_s = self.screen.get_height() - 50
        self.screen.blit(self.high_scores, (x,y))
        self.screen.blit(self.current_score, (x_s, y_s))
    
    def draw_pacman(self) -> None:
        x = 20
        y = self.screen.get_height() - 50
        lives_font = pygame.font.Font(None, 48)
        lives_render = lives_font.render("Lives", True, "white")
        for i in range(self.lives): 
            img = pygame.image.load('assets/pacman.png').convert_alpha()
            img_small = pygame.transform.scale(img, (50, 50))
            self.screen.blit(img_small, (x, y))
            x += 70

    def draw(self):
        self.draw_title()
        self.draw_scores()
        self.draw_pacman()