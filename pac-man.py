"""Main entry point to test maze generation and all entity spawns."""

import sys
import pygame

from config.loader import ConfigLoader
from maze.mazegen import MazeGen
from maze.populate import Populate

# Visual Settings
CELL_SIZE = 40                 
COLOR_BG = (0, 0, 0)           
COLOR_WALL = (36, 36, 255)     
COLOR_PLAYER = (255, 255, 0)   
COLOR_GHOST = (255, 0, 0)      
COLOR_PACGUM = (255, 184, 174) # Peach color
COLOR_SUPER = (255, 255, 255)  # White

WALL_THICKNESS = 4


def draw_raw_maze(screen: pygame.Surface, arr: list[list[int]]) -> None:
    height = len(arr)
    width = len(arr[0]) if height > 0 else 0

    for row in range(height):
        for col in range(width):
            val = arr[row][col]
            x = col * CELL_SIZE
            y = row * CELL_SIZE

            if val & 1: # North
                pygame.draw.line(screen, COLOR_WALL, (x, y), (x + CELL_SIZE, y), WALL_THICKNESS)
            if val & 2: # East
                pygame.draw.line(screen, COLOR_WALL, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), WALL_THICKNESS)
            if val & 4: # South
                pygame.draw.line(screen, COLOR_WALL, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), WALL_THICKNESS)
            if val & 8: # West
                pygame.draw.line(screen, COLOR_WALL, (x, y), (x, y + CELL_SIZE), WALL_THICKNESS)


def draw_pacgums(screen: pygame.Surface, positions: list[tuple[int, int]]) -> None:
    """Draws standard pac-gums as small dots."""
    for row, col in positions:
        cx = col * CELL_SIZE + (CELL_SIZE // 2)
        cy = row * CELL_SIZE + (CELL_SIZE // 2)
        pygame.draw.circle(screen, COLOR_PACGUM, (cx, cy), int(CELL_SIZE * 0.1))


def draw_super_pacgums(screen: pygame.Surface, positions: list[tuple[int, int]]) -> None:
    """Draws super pac-gums as larger white dots."""
    for row, col in positions:
        cx = col * CELL_SIZE + (CELL_SIZE // 2)
        cy = row * CELL_SIZE + (CELL_SIZE // 2)
        pygame.draw.circle(screen, COLOR_SUPER, (cx, cy), int(CELL_SIZE * 0.25))


def draw_ghosts(screen: pygame.Surface, positions: list[tuple[int, int]]) -> None:
    """Draws ghosts as red circles."""
    for row, col in positions:
        cx = col * CELL_SIZE + (CELL_SIZE // 2)
        cy = row * CELL_SIZE + (CELL_SIZE // 2)
        pygame.draw.circle(screen, COLOR_GHOST, (cx, cy), int(CELL_SIZE * 0.35))


def draw_player(screen: pygame.Surface, player_pos: tuple[int, int]) -> None:
    """Draws the player as a yellow circle."""
    row, col = player_pos
    cx = col * CELL_SIZE + (CELL_SIZE // 2)
    cy = row * CELL_SIZE + (CELL_SIZE // 2)
    pygame.draw.circle(screen, COLOR_PLAYER, (cx, cy), int(CELL_SIZE * 0.4))


def main() -> None:
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config_file.json"
    print(f"[+] Loading config from {config_path}...")
    loader = ConfigLoader(config_path)
    config = loader.load()

    levels_data = []
    
    for index, level_cfg in enumerate(config.levels):
        seed = config.seed if index == 0 else 0
        
        maze_gen = MazeGen(width=level_cfg.width, height=level_cfg.height)
        arr = maze_gen.generate(seed=seed)
        
        populate = Populate(arr, level_cfg.width, level_cfg.height)
        
        levels_data.append({
            "index": index + 1,
            "arr": arr,
            "player": populate.find_player_spawn(),
            "ghosts": populate.find_ghosts_spawn(),
            "pacgums": populate.find_pacgum_spawn(),
            "supers": populate.find_superpacgum_spawn(),
            "width": level_cfg.width,
            "height": level_cfg.height
        })

    pygame.init()
    clock = pygame.time.Clock()
    current_level_idx = 0

    def load_level_display(idx: int) -> pygame.Surface:
        data = levels_data[idx]
        window_size = (data["width"] * CELL_SIZE, data["height"] * CELL_SIZE)
        screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption(f"Level {data['index']} | SPACE for next")
        return screen

    screen = load_level_display(current_level_idx)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_SPACE, pygame.K_RIGHT):
                    current_level_idx = (current_level_idx + 1) % len(levels_data)
                    screen = load_level_display(current_level_idx)
                elif event.key == pygame.K_LEFT:
                    current_level_idx = (current_level_idx - 1) % len(levels_data)
                    screen = load_level_display(current_level_idx)

        screen.fill(COLOR_BG)

        current_data = levels_data[current_level_idx]
        
        # Draw in order from bottom to top
        draw_raw_maze(screen, current_data["arr"])
        draw_pacgums(screen, current_data["pacgums"])
        draw_super_pacgums(screen, current_data["supers"])
        draw_ghosts(screen, current_data["ghosts"])
        draw_player(screen, current_data["player"])

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()