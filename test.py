from maze.mazegen import MazeGen
from ui.app import AppRender
from ui.mazedrawer import MazeDrawer
from ui.title import TitleDrawer
if __name__ == "__main__":

    render = AppRender()
    maze = MazeGen(35,25)
    title = TitleDrawer(render.screen)
    mazerender = MazeDrawer(render.screen, maze, 42) 
    render.screen_render(mazerender, title)