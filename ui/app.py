"""
    Module is to load a screen surface and draw into it.
    And this using pygame
"""


import pygame
from ui.mazedrawer import MazeDrawer 
from ui.title import TitleDrawer
from model.player import Player
from model.movement import Movement, Direction

class AppRender:

    def __init__(self):
        """Intialization of the screen with the pygame module
        """

        pygame.init()
        self.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.clock = pygame.time.Clock = pygame.time.Clock()
        # get screen height and width
        self.screen_w = self.screen.get_width()
        self.screen_h = self.screen.get_height()

    

    def draw_player(self, player: Player, cell_size: int, maze_pose: tuple[int, int], i: int) -> None:
        x, y = player.get_world_position()
        maze_x, maze_y = maze_pose
        cx =  maze_x  + int(x * cell_size) + cell_size // 2
        cy =  maze_y  + int(y * cell_size) + cell_size // 2
        

        pygame.draw.circle(self.screen, "gold", (cx, cy), cell_size * 0.3)
        radius = int(cell_size * 0.3)
        if player.direction == Direction.NORTH:
            pygame.draw.polygon(
                self.screen,
                "black", [(cx, cy),
                          (cx + i, cy - radius),
                          (cx - i, cy - radius)
                        ])
        elif player.direction == Direction.SOUTH:
            pygame.draw.polygon(
                self.screen,
                "black", [(cx, cy),
                          (cx + i, cy + radius),
                          (cx - i, cy + radius)
                        ])
        
        elif player.direction == Direction.EAST:
            pygame.draw.polygon(
                self.screen,
                "black", [(cx, cy),
                          (cx + radius, cy - i),
                          (cx + radius, cy + i)
                        ])
        
        elif player.direction == Direction.WEST:
            pygame.draw.polygon(
                self.screen,
                "black", [(cx, cy),
                          (cx - radius, cy - i),
                          (cx - radius, cy + i)
                        ])



    def draw_pacgums(self, positions: list[tuple[int, int]], cell_size: int) -> None:
        for row, col in positions:
            cx = col * cell_size + cell_size // 2
            cy = row * cell_size + cell_size // 2
            pygame.draw.circle(self.screen, (255, 184, 174), (cx, cy), int(cell_size * 0.4))
        
    def handle_event(self, event: pygame.event.Event, player: Player) -> None:
        if event.key in (pygame.K_UP, pygame.K_w):
            player.set_direction(Direction.NORTH)
        if event.key in (pygame.K_DOWN, pygame.K_s):
            player.set_direction(Direction.SOUTH)
        if event.key in (pygame.K_LEFT, pygame.K_a):
            player.set_direction(Direction.WEST)
        if event.key in (pygame.K_RIGHT, pygame.K_d):
            player.set_direction(Direction.EAST)
    
    def screen_render(self, mazedrawer: MazeDrawer, title: TitleDrawer, player: Player):
        """
            Instance method to draw the surface screen.
        """

        # to draw we might have variable runing the loop
        run = True
        mouv_sys = Movement()
        cell_size = mazedrawer.get_cell_size()  
        maze_size = mazedrawer.get_start_position(cell_size)
        i = 0
        while run:
            dt = self.clock.tick(60) / 1000.0
            
            # get the event from the screen rendered
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                
                    if event.key == pygame.K_ESCAPE:

                        run = False
                    else:
                        self.handle_event(event, player)
            if i == 0:
                direction = 1
            if i == 10:
                direction = -1

            i += direction 
            self.screen.fill("black")
            title.draw()
            mazedrawer.draw_maze()
            player.update(dt, mouv_sys, mazedrawer.grid)
            self.draw_player(player, cell_size, maze_size, i)
            pygame.display.flip()

        pygame.quit()


