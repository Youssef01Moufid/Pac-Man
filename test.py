from maze.mazegen import MazeGen
from ui.app import AppRender
from ui.mazedrawer import MazeDrawer
from ui.title import TitleDrawer
from maze.populate import Populate
from config.loader import ConfigLoader
from model.player import Player
import sys
import pygame


# def draw_pacgums(screen: pygame.Surface, positions: list[tuple[int, int]])


if __name__ == "__main__":
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config_file.json"
    loader = ConfigLoader(config_path)
    config = loader.load()
    level_cfg = config.levels[0]
    maze_gen = MazeGen(width=level_cfg.width, height=level_cfg.height)
    arr = maze_gen.generate(seed=config.seed)
    
    render = AppRender()
    populate = Populate(arr, width=level_cfg.width, height=level_cfg.height)
    
    spawn = populate.find_player_spawn()
    player = Player(position=spawn)
    
    title = TitleDrawer(render.screen)
    
    mazerender = MazeDrawer(render.screen, arr, 42) 
    
    render.screen_render(mazerender, title, player, populate.find_pacgum_spawn())
