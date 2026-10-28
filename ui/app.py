"""
    Module is to load a screen surface and draw into it.
    And this using pygame
"""


import pygame
from ui.mazedrawer import MazeDrawer 
from ui.title import TitleDrawer
from ui.scene import SceneManger

class AppRender:

    def __init__(self):
        """Intialization of the screen with the pygame module
        """


        pygame.init()
        self.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        
        self.clock = pygame.time.Clock = pygame.time.Clock()
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
            
            title.draw()
            mazedrawer.draw_maze()
            pygame.display.flip()

        pygame.quit()


# class App:
#     """ Render screen """

#     def __init__(self):
#         """ Initialization for pygame """
#         pygame.init()
#         self.screen = pygame.display.set_mode(pygame.FULLSCREEN)
#         self.time = pygame.time.Clock()
#         self.manager = 

#     def run(self):
#         ...

# class App:
#     def __init__(self):
        
