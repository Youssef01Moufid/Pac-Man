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
        self.rect_w = self.sc_w // 3
        self.rect_h = self.sc_h // 2

        
    def get_cell_size(self) -> int:
        """ instance method the generate the cell size """
        

        # get how many rows and cols
        rows = len(self.grid)
        cols = len(self.grid[0])

        return min(self.rect_w // cols, self.rect_h // rows)

    def get_start_position(self) -> tuple[int, int]:
        "Instance method to get the start position to draw the grid"
        return (self.sc_w - self.rect_w) // 2, (self.sc_h - self.rect_h) // 2
        


    def draw_walls(self, cell_size: int):
        
        N,E,S,W = 1,2,4,8
        
        x_start, y_start = self.get_start_position()

        
        for row, rows in enumerate(self.grid):
            for col, cell in enumerate(rows):

                x = x_start  + (col * cell_size)
                y = y_start + (row * cell_size)
                
                if cell == 15:
                    pygame.draw.rect(
                        self.screen,
                        'blue',
                        (x, y, cell_size, cell_size)
                    )

                if cell & N:
                    pygame.draw.line(
                        self.screen,
                        'white',
                        (x, y),
                        (x + cell_size, y)
                    )

                if cell & E:
                    pygame.draw.line(
                        self.screen,
                        'white',
                        (x + cell_size, y),
                        (x + cell_size, y + cell_size)
                    )
                if cell & S:
                    pygame.draw.line(
                        self.screen,
                        'white',
                        (x + cell_size, y + cell_size),
                        (x, y + cell_size)
                    )

                if cell & W:
                    pygame.draw.line(
                        self.screen,
                        'white',
                        (x, y + cell_size),
                        (x, y)
                    )
    
    def draw_maze(self):
        """
            Instance method to draw the entire Maze
        """
        
        cell_size = self.get_cell_size()
        self.draw_walls(cell_size)
        

        
