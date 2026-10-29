from maze.mazegen import MazeGen
from ui.app import AppRender
from ui.mazedrawer import MazeDrawer
from ui.title import TitleDrawer
from maze.populate import Populate

from model.player import Player

import pygame


# def draw_pacgums(screen: pygame.Surface, positions: list[tuple[int, int]])


if __name__ == "__main__":

    render = AppRender()
    maze = MazeGen(35,25)
    grid = maze.generate(42)
    populate = Populate(grid, width=35, height=25)
    spawn = populate.find_player_spawn()
    player = Player(position=spawn)
    
    title = TitleDrawer(render.screen)
    
    mazerender = MazeDrawer(render.screen, grid, 42) 
    
    render.screen_render(mazerender, title, player)
