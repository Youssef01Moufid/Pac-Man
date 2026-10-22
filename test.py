from maze.mazegen import MazeGen
from ui.app import AppRender
from ui.mazedrawer import MazeDrawer

if __name__ == "__main__":

    render = AppRender()
    maze = MazeGen(25,25)
    mazerender = MazeDrawer(render.screen, maze, 42) 
    render.screen_render(mazerender)