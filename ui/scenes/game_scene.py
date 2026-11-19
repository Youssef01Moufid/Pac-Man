from ui.hud import Hud
from ui.scene import Scene
from ui.scene_manager import SceneManager
from game.gamestate import GameState
import pygame
from model.player import Direction
from config.model import Config
from game.gamestate import GameStatus
from model.ghost import GhostType, GhostState

import os
import math

FONT_URL = os.path.join('assets', 'fonts', 'PressStart2P-Regular.ttf')

class GameScene(Scene):

    PACMAN_ANIMATION = 20.0
    DIRECTION = 4.0
    def __init__(
            self,
            manager: SceneManager,
            width : int,
            height: int,
            game: GameState,
            config: Config,
            ) -> None:
        super().__init__(manager)
        self.width = width
        self.height = height
        self.game = game
        self.hud = Hud(self.game)
        self.config = config

    def handle_events(self, event: pygame.event.Event) -> None:
        """ Handle event from the app and send it into the game """
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_p, pygame.K_ESCAPE):
            from ui.scenes.pause_scene import PauseScene
            if self.game.status == GameStatus.PLAYING:
                self.game.pause()
            self.manager.push(PauseScene(self.manager, self.width, self.height, self.game,self.config))
        
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.game.set_player_direction(Direction.NORTH)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.game.set_player_direction(Direction.SOUTH)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.game.set_player_direction(Direction.EAST)
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.game.set_player_direction(Direction.WEST)
            
            elif event.key == pygame.K_F1:
                self.game.toggle_ghost_freeze()
            
            elif event.key == pygame.K_F2:
                self.game.toggle_speed_boost()
            
            elif event.key == pygame.K_F3:
                self.game.skip_level()

            elif event.key == pygame.K_n:
                if self.game.status == GameStatus.LEVEL_COMPLETE:
                    self.game.next_level()



    def update(self, dt: float) -> None:
        """"""
        # try:
        if self.game.status in  (GameStatus.GAME_WON, GameStatus.GAME_OVER):
            from ui.scenes.mainmenu_scene import MainMenuScene
            self.manager.replace(MainMenuScene(self.manager, self.width, self.height, self.config))
        self.game.update(dt)

        # if self.game.is_over:
        #     from ui.scenes.mainmenu_scene import MainMenuScene
        #     self.manager.replace(MainMenuScene(self.manager, self.width, self.height))
    

    def _get_cell_size(self, surface: pygame.Surface) -> int:
        """ Choose the small size width and heigh to get cell size """
        w, h = surface.get_size()
        rect_w, rect_h = int(w - (w // 6)), int(h - (h // 6))

        rows = len(self.game.level.maze)
        cols = len(self.game.level.maze[0])
        return min(int(rect_w // cols), int(rect_h // rows))

    def _get_start_position(self, sc_w: int, sc_h: int, cell: int) -> tuple[int, int]:
        """return start position for the maze """
        maze = self.game.level.maze
        rows = len(maze)
        cols = len(maze[0])
        maze_w, maze_h = cols * cell, rows * cell
        return (sc_w - maze_w) // 2, (sc_h - maze_h) // 2

    def draw_wall(self, surface: pygame.Surface, p1: tuple[int, int], p2: tuple[int, int], thickness: int) -> None:
        """draw line and round the corner"""
        pygame.draw.line(surface, "grey", p1, p2, thickness)
        pygame.draw.circle(surface, "grey", p1, thickness // 2.5)
        pygame.draw.circle(surface, "grey", p2, thickness // 2.5)

    def _draw_walls(self, surface: pygame.Surface, cell_size: int) -> None:
        """ Draw The maze walls North, East, South and West"""
        N, E, S, W = 1, 2, 4, 8
        screen_w, screen_h = surface.get_size()
        x_start, y_start = self._get_start_position(screen_w, screen_h, cell_size)
        maze = self.game.level.maze
        for row, rows in enumerate(maze):
            for col, cell in enumerate(rows):
                x = x_start + (col * cell_size)
                y = y_start + (row * cell_size)

                if cell == 15:
                    pygame.draw.rect(
                        surface,
                        'lightyellow',
                        (x, y, cell_size, cell_size)
                    )
                
                if cell & N:
                    self.draw_wall(surface, (x, y), (x + cell_size, y), 5)
                if cell & E:
                    self.draw_wall(surface, (x + cell_size, y), (x + cell_size, y + cell_size), 5)
                if cell & S:
                    self.draw_wall(surface, (x + cell_size, y + cell_size), (x, y + cell_size), 5)
                if cell & W:
                    self.draw_wall(surface, (x, y + cell_size), (x, y), 5)
        

    def draw_maze(self, surface: pygame.Surface) -> None:
        """ Draw the walls and floors where pacman and ghosts lives """
        w, h = surface.get_size()
        cell_size = self._get_cell_size(surface)
        self._draw_walls(surface, cell_size)

    def draw_frames(self, surface: pygame.Surface) -> None:
        """ fill the screen and border in the surface"""
        surface.fill((0, 0, 0))
        w, h = surface.get_size()
        outter = pygame.Rect(0, 0, w - 24, h - 24)
        inner = outter.inflate(-12, -12)
        pygame.draw.rect(surface, 'blue', outter, width=3, border_radius=14)
        pygame.draw.rect(surface, 'blue', inner, width=2, border_radius=8)


    def draw_pacman(self, surface: pygame.Surface) -> None:
        """ draw just circle first """
        pacman = self.game.player
        x, y = pacman.get_world_position()
        cell = self._get_cell_size(surface)
        w, h = surface.get_size()
        x_start, y_start = self._get_start_position(w, h, cell)
        cx = int(x_start + (x * cell) + cell / 2)
        cy = int(y_start + (y * cell) + (cell / 2))
        
        radius = int(cell * 0.35)
        pygame.draw.circle(
            surface,
            "yellow",
            (cx, cy),
            int(cell * 0.3)
        )
        if self.PACMAN_ANIMATION == 20.0:
            self.DIRECTION = -2.5
        if self.PACMAN_ANIMATION == 0.0:
            self.DIRECTION = 2.5

        self.PACMAN_ANIMATION += self.DIRECTION
        i = self.PACMAN_ANIMATION
        radius = int(cell * 0.3)
        if pacman.direction == Direction.NORTH:
            pygame.draw.polygon(
                surface,
                "black", [(cx, cy),
                          (cx + i, cy - radius),
                          (cx - i, cy - radius)
                        ])
        elif pacman.direction == Direction.SOUTH:
            pygame.draw.polygon(
                surface,
                "black", [(cx, cy),
                          (cx + i, cy + radius),
                          (cx - i, cy + radius)
                        ])
        
        elif pacman.direction == Direction.EAST:
            pygame.draw.polygon(
                surface,
                "black", [(cx, cy),
                          (cx + radius, cy - i),
                          (cx + radius, cy + i)
                        ])
        
        elif pacman.direction == Direction.WEST:
            pygame.draw.polygon(
                surface,
                "black", [(cx, cy),
                          (cx - radius, cy - i),
                          (cx - radius, cy + i)
                        ])

    def draw_eyes(
        self,
        surface: pygame.Surface,
        cx: int,
        cy: int,
        r: float) -> None:
        """ Draw the eyes for the ghosts """
        
        eye_w = int(r * 0.55)
        eye_h = int(r * 0.65)
        pupil_radius = int(r * 0.15)

        for side in (-1, 1):
            eye_x = cx + side * r * 0.38
            eye_y = cy - r * 0.15

            eye = pygame.Rect(0, 0, eye_w, eye_h)
            eye.center = (int(eye_x), int(eye_y))

            pygame.draw.ellipse(
                surface,
                (255, 255, 255),
                eye,
            )
            pygame.draw.circle(
                surface,
                (33, 33, 200),
                (int(eye_x), int(eye_y)),
                pupil_radius,
            )

    def draw_ghost(
        self,
        surface: pygame.Surface,
        cx: int,
        cy: int,
        r: float,
        color: str
        ) -> None:
        """ Draw the shape of the ghost"""
        points = []
        # head
        steps = 16
        for i in range(steps + 1):
            angle = math.pi * i / steps
            x = cx - r * math.cos(angle)
            y = cy - r * math.sin(angle)

            points.append((x, y))
        bottom = cy + r
        points.append((cx + r, bottom))
        waves = 6
        for i in range(1, waves + 1):
            x = cx + r - i * (2 * r / waves)

            if i % 2 == 1:
                y = bottom - r * 0.3
            else:
                y = bottom
            points.append((x, y))

        pygame.draw.polygon(surface, color, points)

    def draw_ghosts(self, surface: pygame.Surface) -> None:
        """ Draw ghost ans cirle with colors"""
        ghosts = self.game.ghosts
        cell = self._get_cell_size(surface)
        w, h = surface.get_size()
        x_start, y_start = self._get_start_position(w, h, cell)
        for ghost in ghosts:
            x, y = ghost.get_world_position()
            if ghost.state == GhostState.NORMAL:
                if ghost.ghost_type == GhostType.RED:
                    color = "red"
                elif ghost.ghost_type == GhostType.PINK:
                    color = "pink"
                elif ghost.ghost_type == GhostType.ORANGE:
                    color = "orange"
                elif ghost.ghost_type == GhostType.CYAN:
                    color = "cyan"
            elif ghost.state == GhostState.FRIGHTENED:
                    color = "blue"
            
            elif GhostState == GhostState.EATEN:
                color = "white"
            
            else:
                color = "grey"
            
            
            px = int(x_start + (x * cell) + cell / 2)
            py = int(y_start + (y * cell) + cell / 2)
            r = cell * 0.3
            self.draw_ghost(surface, px, py, r, color)
            self.draw_eyes(surface, px, py, r)


    def draw_pacgums(self, surface: pygame.Surface) -> None:
        """ draw pacgums with """
        cell = self._get_cell_size(surface)
        w, h = surface.get_size()
        x_start, y_start = self._get_start_position(w, h, cell)
        for pacgum in self.game.level.pacgums:
            y, x = pacgum
            cx = int(x_start + (x * cell) + cell / 2)
            cy = int(y_start + (y * cell) + cell / 2)
            r = cell * 0.1
            rect = pygame.Rect(cx, cy, r, r)
            pygame.draw.rect(
                surface,
                "thistle1",
                rect
            )

    def draw_super_pacgums(self, surface: pygame.Surface) -> None:
        """ draw the superpacgame in the corner """
        super_pacgums = self.game.level.super_pacgums
        cell = self._get_cell_size(surface)
        w, h = surface.get_size()
        x_start, y_start = self._get_start_position(w, h, cell)
        for pac in super_pacgums:
            y, x = pac
            cx = int(x_start + (x * cell) + cell / 3)
            cy = int(y_start + (y * cell) + cell / 3)
            r = cell * 0.2
            rect = pygame.Rect(cx, cy, r, r)
            pygame.draw.rect(
                surface,
                "white",
                rect
            )


    def draw_status_message(self, surface: pygame.Surface) -> None:
        """ Status to pass to the next """
        if self.game.status == GameStatus.LEVEL_COMPLETE:
            try:
                font = pygame.font.Font(FONT_URL, 24)
            except Exception:
                font = pygame.font.Font(None, 24)

            message = "LEVEL COMPLETE - Press N"
            cell = self._get_cell_size(surface)
            maze_height = len(self.game.level.maze) * cell
            overlay = pygame.Surface(
                (surface.get_width(), surface.get_height()),
                pygame.SRCALPHA
            )
            overlay.fill((0, 0, 0, 170))
            surface.blit(overlay, (0, 0))
            x = font.render(
                message,
                True,
                "yellow"
            )
            rect = x.get_rect(
                center=(
                    surface.get_width() // 2,
                    surface.get_height() // 2,
                )
            )
            surface.blit(x, rect)

    def draw(self, surface: pygame.Surface) -> None:

        self.draw_frames(surface)
        self.draw_maze(surface)
        self.draw_super_pacgums(surface)
        self.draw_pacgums(surface)
        self.draw_pacman(surface)
        self.draw_ghosts(surface)
        self.draw_status_message(surface)
        self.hud.draw(surface)