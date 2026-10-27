"""Main entry point to test maze generation, entity spawns, and Player movement."""

import sys
import pygame

from config.loader import ConfigLoader
from maze.mazegen import MazeGen
from maze.populate import Populate

# Adjust these imports if your folder structure differs
from model.movement import Direction, Movement
from model.player import Player

# Visual settings
CELL_SIZE = 40
COLOR_BG = (0, 0, 0)
COLOR_WALL = (36, 36, 255)
COLOR_PLAYER = (255, 255, 0)
COLOR_GHOST = (255, 0, 0)
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

            if val & 1:  # North
                pygame.draw.line(screen, COLOR_WALL, (x, y), (x + CELL_SIZE, y), WALL_THICKNESS)
            if val & 2:  # East
                pygame.draw.line(screen, COLOR_WALL, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), WALL_THICKNESS)
            if val & 4:  # South
                pygame.draw.line(screen, COLOR_WALL, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), WALL_THICKNESS)
            if val & 8:  # West
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


def draw_ghosts(screen: pygame.Surface, positions: list[tuple[int, int]]) -> None:
    for row, col in positions:
        cx = col * CELL_SIZE + CELL_SIZE // 2
        cy = row * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, COLOR_GHOST, (cx, cy), int(CELL_SIZE * 0.35))


def draw_player(screen: pygame.Surface, world_position: tuple[float, float]) -> None:
    # The refactored Player class now returns (x, y) natively (col, row)
    tile_x, tile_y = world_position
    
    cx = int(tile_x * CELL_SIZE) + (CELL_SIZE // 2)
    cy = int(tile_y * CELL_SIZE) + (CELL_SIZE // 2)
    
    pygame.draw.circle(screen, COLOR_PLAYER, (cx, cy), int(CELL_SIZE * 0.4))


def main() -> None:
    # 1. Load Config & Maze
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config_file.json"
    loader = ConfigLoader(config_path)
    config = loader.load()

    level_cfg = config.levels[0]
    maze_gen = MazeGen(width=level_cfg.width, height=level_cfg.height)
    arr = maze_gen.generate(seed=config.seed)

    populate = Populate(arr, level_cfg.width, level_cfg.height)
    
    # 2. Init Pygame Display
    pygame.init()
    window_size = (level_cfg.width * CELL_SIZE, level_cfg.height * CELL_SIZE)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Pac-Man Engine - Refactored Player Test")
    clock = pygame.time.Clock()

    # 3. Instantiate Engine Systems
    movement_sys = Movement()
    
    # Initialize the Player with the single position tuple requested by __init__
    player_spawn_tuple = populate.find_player_spawn()
    player = Player(position=player_spawn_tuple, speed=5.0)

    # 4. Game Loop
    running = True
    while running:
        # Calculate Delta Time (dt) in seconds for smooth movement
        dt = clock.tick(60) / 1000.0

        # FRONT-END: Capture Inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                # Check for either the Arrow Keys or WASD Keys
                elif event.key in (pygame.K_UP, pygame.K_w):
                    player.set_direction(Direction.NORTH)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    player.set_direction(Direction.SOUTH)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    player.set_direction(Direction.WEST)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    player.set_direction(Direction.EAST)

        # BACK-END: Update Engine Logic
        # Advance the physics; we can ignore the returned `arrived` list for this movement test
        _ = player.update(dt, movement_sys, arr)

        # FRONT-END: Render Frame
        screen.fill(COLOR_BG)
        
        draw_raw_maze(screen, arr)
        draw_pacgums(screen, populate.find_pacgum_spawn())
        draw_super_pacgums(screen, populate.find_superpacgum_spawn())
        draw_ghosts(screen, populate.find_ghosts_spawn())
        
        # Request exact floating-point (x, y) coordinates from the engine
        draw_player(screen, player.get_world_position())

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()