"""Main entry point for the Pac-Man game."""

import sys
import logging
import pygame
from pathlib import Path

# Adjust imports based on your project structure
from config.loader import ConfigLoader
from maze.adapter import MazeAdapter
from maze.grid import TileGrid

# --- Configuration & Colors ---
TILE_SIZE = 24  # Size of each square in pixels
FPS = 60

COLOR_BG = (0, 0, 0)          # Black floor
COLOR_WALL = (33, 33, 255)    # Classic Pac-Man Blue


def draw_maze(screen: pygame.Surface, grid: TileGrid) -> None:
    """Renders the TileGrid onto the Pygame surface."""
    for row in range(grid.height):
        for col in range(grid.width):
            # Calculate pixel coordinates
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            
            # Create a rectangle for the tile
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            
            if not grid.is_floor(row, col):
                # Draw solid blue block for walls
                pygame.draw.rect(screen, COLOR_WALL, rect)
                
                # Optional: draw a slightly darker inner border for depth
                pygame.draw.rect(screen, (20, 20, 150), rect, width=2)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    # 1. Load the first level from the configuration
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config_file.json"
    loader = ConfigLoader(config_path)
    config = loader.load()
    level = config.levels[0]

    # 2. Generate the maze using the adapter
    # If the generator fails, the adapter safely returns the 11x11 fallback
    adapter = MazeAdapter(width=level.width, height=level.height)
    grid = adapter.generate(seed=config.seed)

    # 3. Initialize Pygame
    pygame.init()
    
    # Calculate window size dynamically based on the generated grid
    window_width = grid.width * TILE_SIZE
    window_height = grid.height * TILE_SIZE
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption(f"Pac-Man - Level 1 ({grid.width}x{grid.height})")
    
    clock = pygame.time.Clock()

    # 4. Main Game Loop
    running = True
    while running:
        # Event handling (Keyboard/Mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Rendering
        screen.fill(COLOR_BG)          # Clear the screen to black
        draw_maze(screen, grid)        # Draw the walls
        
        pygame.display.flip()          # Swap the display buffer to screen
        clock.tick(FPS)                # Limit frame rate to 60 FPS

    # 5. Cleanup
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()