import pygame



class TitleDrawer:
    def __init__(
            self,
            screen: pygame.Surface
        ):
        self.screen = screen
        self.title_font = pygame.font.Font(None, 48)
        self.title_surf = self.title_font.render("PAC-MAN", True, "yellow")


    
    def draw_title(self) -> None:

        # distance = self.screen.get_width() // 2 - 
        rect = self.title_surf.get_rect(midtop=(self.screen.get_width() // 2, 10))
        rect.centery = self.screen.get_height() // 17
        self.screen.blit(self.title_surf, rect)