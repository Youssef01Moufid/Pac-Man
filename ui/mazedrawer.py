"""
The goal from this class is to draw the maze into pygame surface
"""

import pygame
from maze.mazegen import MazeGen


class MazeDrawer:
    
    def __init__(self, screen: pygame.Surface, maze: MazeGen, seed: int):
        """
            Initialize the MazeDrawer
        """
        
        self.screen = screen
        # getting screen size from the screen surface
        self.sc_w = self.screen.get_width()
        self.sc_h = self.screen.get_height()

        self.grid = maze.generate(seed)

        # getting the rectangle holder for the grid
        self.rect_w = self.sc_w  - (self.sc_w // 5)
        self.rect_h = self.sc_h  - (self.sc_h // 5)

        
    def get_cell_size(self) -> int:
        """ instance method the generate the cell size """
        rows = len(self.grid)
        cols = len(self.grid[0])
        return min(int(self.rect_w// cols), int(self.rect_h// rows))

    def get_start_position(self, cell_size: int) -> tuple[int, int]:
        "Instance method to get the start position to draw the grid"
        rows = len(self.grid)
        cols = len(self.grid[0])
        maze_w, maze_h = cols * cell_size, rows * cell_size
        return (self.sc_w - maze_w) // 2, (self.sc_h - maze_h) // 2
        

    def draw_wall(self, p1: tuple[int, int], p2: tuple[int, int], thickness: int) -> None:
        """ Instance method draw the wall """

        pygame.draw.line(self.screen, "grey",p1, p2, thickness)
        pygame.draw.circle(self.screen, "grey", p1, thickness // 2.5)
        pygame.draw.circle(self.screen, "grey", p2, thickness // 2.5)




    def draw_walls(self, cell_size: int) -> None:
        """Instance method checks if wall exist and draw the wall
        """
        N,E,S,W = 1,2,4,8
        
        x_start, y_start = self.get_start_position(cell_size)


        for row, rows in enumerate(self.grid):
            for col, cell in enumerate(rows):
                
                x = x_start  + (col * cell_size)
                y = y_start + (row * cell_size)

                if cell == 15:
                    pygame.draw.rect(
                        self.screen,
                        'lightyellow',
                        (x, y, cell_size, cell_size)
                    )

                if cell & N:
                    self.draw_wall((x, y), (x + cell_size, y), 5)


                if cell & E:
                    self.draw_wall((x + cell_size, y), (x + cell_size, y + cell_size), 5)
                
                if cell & S:
                    self.draw_wall((x + cell_size, y + cell_size), (x, y + cell_size), 5)

                if cell & W:
                    self.draw_wall((x, y + cell_size), (x, y), 5)

    
    def draw_maze(self) -> None:
        """
            Instance method to draw the entire Maze
        """
        cell_size = self.get_cell_size()
        self.draw_walls(cell_size)
        

        
