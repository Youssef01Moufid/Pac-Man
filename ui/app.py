"""
    Module is to load a screen surface and draw into it.
    And this using pygame
"""


import pygame
from ui.mazedrawer import MazeDrawer 
from ui.title import TitleDrawer
class AppRender:

    def __init__(self):
        """Intialization of the screen with the pygame module
        """


        pygame.init()
        self.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        
        
        # get screen height and width
        self.screen_w = self.screen.get_width()
        self.screen_h = self.screen.get_height()

    
    def screen_render(self, mazedrawer: MazeDrawer, title: TitleDrawer):
        """
            Instance method to draw the surface screen.
        """

        # to draw we might have variable runing the loop
        run = True
        
        while run:
            
            # get the event from the screen rendered
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                
                    if event.key == pygame.K_ESCAPE:

                        run = False
            title.draw_title()
            mazedrawer.draw_maze()
            pygame.display.flip()

        pygame.quit()


