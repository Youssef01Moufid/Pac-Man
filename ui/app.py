"""
    Module is to load a screen surface and draw into it.
    And this using pygame
"""


import pygame
from maze.mazegen import MazeGen
from ui.mazedrawer import MazeDrawer 

class AppRender:

    def __init__(self):
        """Intialization of the screen with the pygame module
        """


        pygame.init()
        self.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        
        
        # get screen height and width
        self.screen_w = self.screen.get_width()
        self.screen_h = self.screen.get_height()

    
    def screen_render(self, mazedrawer: MazeDrawer):
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

                        print(f"Width screen: {self.screen_w} px")
                        print(f"Height screen: {self.screen_h} px")
                        run = False

            mazedrawer.draw_maze()
            pygame.display.flip()

        pygame.quit()


