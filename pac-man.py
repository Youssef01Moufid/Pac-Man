"""Main entry point to test maze generation, entity spawns, and Player movement only."""

import sys
import pygame

from config.loader import ConfigLoader
from maze.mazegen import MazeGen
from maze.populate import Populate

from model.movement import Direction, Movement
from model.player import Player

# Visual settings
CELL_SIZE = 40
COLOR_BG = (0, 0, 0)
COLOR_WALL = (36, 36, 255)
COLOR_PLAYER = (255, 255, 0)
COLOR_PACGUM = (255, 184, 174)
COLOR_SUPER = (255, 255, 255)
WALL_THICKNESS = 4


def draw_raw_maze(screen: pygame.Surface, arr: list[list[int]]) -> None:
    height = len(arr)
    width = len(arr[0]) if height > 0 else 0

    for row in range(height):
        for col in range(width):
            val = arr[row][col]
            x = col * CELL_SIZE
            y = row * CELL_SIZE

            if val & 1:
                pygame.draw.line(screen, COLOR_WALL, (x, y), (x + CELL_SIZE, y), WALL_THICKNESS)
            if val & 2:
                pygame.draw.line(screen, COLOR_WALL, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), WALL_THICKNESS)
            if val & 4:
                pygame.draw.line(screen, COLOR_WALL, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), WALL_THICKNESS)
            if val & 8:
                pygame.draw.line(screen, COLOR_WALL, (x, y), (x, y + CELL_SIZE), WALL_THICKNESS)


def draw_pacgums(screen: pygame.Surface, positions: list[tuple[int, int]]) -> None:
    for row, col in positions:
        cx = col * CELL_SIZE + CELL_SIZE // 2
        cy = row * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, COLOR_PACGUM, (cx, cy), int(CELL_SIZE * 0.1))


def draw_super_pacgums(screen: pygame.Surface, positions: list[tuple[int, int]]) -> None:
    for row, col in positions:
        cx = col * CELL_SIZE + CELL_SIZE // 2
        cy = row * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, COLOR_SUPER, (cx, cy), int(CELL_SIZE * 0.25))


def draw_player(screen: pygame.Surface, world_position: tuple[float, float]) -> None:
    # Player returns (x, y), meaning (col, row).
    tile_x, tile_y = world_position

    cx = int(tile_x * CELL_SIZE) + CELL_SIZE // 2
    cy = int(tile_y * CELL_SIZE) + CELL_SIZE // 2

    pygame.draw.circle(screen, COLOR_PLAYER, (cx, cy), int(CELL_SIZE * 0.4))


def main() -> None:
    # 1. Load Config and Generate Maze
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config_file.json"
    loader = ConfigLoader(config_path)
    config = loader.load()

    level_cfg = config.levels[0]

    maze_gen = MazeGen(width=level_cfg.width, height=level_cfg.height)
    arr = maze_gen.generate(seed=config.seed)

    # 2. Populate the Maze
    populate = Populate(
        arr,
        level_cfg.width,
        level_cfg.height,
        level_cfg.pacgum,
    )

    # Generate spawn positions ONCE.
    player_spawn = populate.find_player_spawn()
    pacgum_positions = populate.find_pacgum_spawn()
    super_pacgum_positions = populate.find_superpacgum_spawn()

    # 3. Initialize Pygame
    pygame.init()

    window_size = (
        level_cfg.width * CELL_SIZE,
        level_cfg.height * CELL_SIZE,
    )

    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Pac-Man Engine - Player Only Test")
    clock = pygame.time.Clock()

    # 4. Initialize Engine Systems
    movement_sys = Movement()

    spawn_row, spawn_col = player_spawn
    player = Player(row=spawn_row, col=spawn_col, speed=5.0)

    # 5. Game Loop
    running = True

    while running:
        dt = clock.tick(60) / 1000.0

        # Capture Inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key in (pygame.K_UP, pygame.K_w):
                    player.set_direction(Direction.NORTH)

                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    player.set_direction(Direction.SOUTH)

                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    player.set_direction(Direction.WEST)

                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    player.set_direction(Direction.EAST)

        # Update Player Movement
        _ = player.update(dt, movement_sys, arr)

        # Render Frame
        screen.fill(COLOR_BG)

        draw_raw_maze(screen, arr)
        draw_pacgums(screen, pacgum_positions)
        draw_super_pacgums(screen, super_pacgum_positions)
        draw_player(screen, player.get_world_position())

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()