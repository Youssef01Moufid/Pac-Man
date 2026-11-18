
"""Test the complete Pac-Man engine using pygame."""

import sys

import pygame

from config.loader import ConfigLoader
from game.gamestate import GameState, GameStatus
from model.ghost import GhostState, GhostType
from model.movement import Direction


CELL_SIZE = 40
WALL_SIZE = 4
HUD_HEIGHT = 125
FPS = 60

BLACK = (0, 0, 0)
BLUE = (36, 36, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
PINK = (255, 184, 174)

GHOST_COLORS = {
    GhostType.RED: (255, 45, 45),
    GhostType.PINK: (255, 130, 190),
    GhostType.CYAN: (0, 225, 235),
    GhostType.ORANGE: (255, 165, 35),
}

KEY_DIRECTIONS = {
    pygame.K_UP: Direction.NORTH,
    pygame.K_RIGHT: Direction.EAST,
    pygame.K_DOWN: Direction.SOUTH,
    pygame.K_LEFT: Direction.WEST,
    pygame.K_w: Direction.NORTH,
    pygame.K_d: Direction.EAST,
    pygame.K_s: Direction.SOUTH,
    pygame.K_a: Direction.WEST,
}


def cell_center(row: float, col: float) -> tuple[int, int]:
    """Convert maze coordinates to screen pixels."""
    return (
        int((col + 0.5) * CELL_SIZE),
        int((row + 0.5) * CELL_SIZE),
    )


def create_screen(game: GameState) -> pygame.Surface:
    """Create a window matching the current level size."""
    height = len(game.level.maze)
    width = len(game.level.maze[0])

    return pygame.display.set_mode(
        (
            width * CELL_SIZE,
            height * CELL_SIZE + HUD_HEIGHT,
        )
    )


def draw_maze(
    screen: pygame.Surface,
    maze: list[list[int]],
) -> None:
    """Draw maze walls from their bitmask values."""
    for row, cells in enumerate(maze):
        for col, value in enumerate(cells):
            x = col * CELL_SIZE
            y = row * CELL_SIZE

            walls = [
                (1, (x, y), (x + CELL_SIZE, y)),
                (
                    2,
                    (x + CELL_SIZE, y),
                    (x + CELL_SIZE, y + CELL_SIZE),
                ),
                (
                    4,
                    (x, y + CELL_SIZE),
                    (x + CELL_SIZE, y + CELL_SIZE),
                ),
                (8, (x, y), (x, y + CELL_SIZE)),
            ]

            for bit, start, end in walls:
                if value & bit:
                    pygame.draw.line(
                        screen, BLUE, start, end, WALL_SIZE
                    )


def draw_collectibles(
    screen: pygame.Surface,
    game: GameState,
) -> None:
    """Draw remaining regular and Super Pac-Gums."""
    for row, col in game.level.pacgums:
        pygame.draw.circle(
            screen,
            PINK,
            cell_center(row, col),
            4,
        )

    for row, col in game.level.super_pacgums:
        pygame.draw.circle(
            screen,
            WHITE,
            cell_center(row, col),
            10,
        )


def draw_entities(
    screen: pygame.Surface,
    game: GameState,
) -> None:
    """Draw Player and Ghosts using smooth world positions."""
    px, py = game.player.get_world_position()

    # Blink after losing a life.
    visible = (
        game.invulnerable_remaining <= 0.0
        or int(game.invulnerable_remaining * 8) % 2 != 0
    )

    if visible:
        pygame.draw.circle(
            screen,
            YELLOW,
            cell_center(py, px),
            int(CELL_SIZE * 0.35),
        )

    for ghost in game.ghosts:
        if ghost.state == GhostState.RESPAWNING:
            continue

        gx, gy = ghost.get_world_position()

        if ghost.state == GhostState.FRIGHTENED:
            color = (40, 90, 255)
        elif ghost.state == GhostState.EATEN:
            color = WHITE
        else:
            color = GHOST_COLORS[ghost.ghost_type]

        pygame.draw.circle(
            screen,
            color,
            cell_center(gy, gx),
            int(CELL_SIZE * 0.3),
        )


def draw_hud(
    screen: pygame.Surface,
    game: GameState,
    font: pygame.font.Font,
) -> None:
    """Show the current game information."""
    top = len(game.level.maze) * CELL_SIZE + 8

    lines = [
        (
            f"Level: {game.level_index + 1}/"
            f"{len(game.config.levels)}"
            f"   Score: {game.score}"
            f"   Lives: {game.lives}"
            f"   Time: {game.time_left:.1f}"
        ),
        (
            f"Pac-Gums: {len(game.level.pacgums)}"
            f"   Super: {len(game.level.super_pacgums)}"
            f"   Status: {game.status.name}"
        ),
        (
            f"Ghost Freeze: {'ON' if game.ghosts_frozen else 'OFF'}"
            f"   Speed Boost: {'ON' if game.speed_boost else 'OFF'}"
        ),
        "F1: Freeze   F2: Speed   F3: Skip   N: Next",
        "WASD/Arrows: Move   P: Pause   R: Restart   ESC: Quit",
    ]

    for index, line in enumerate(lines):
        text = font.render(line, True, WHITE)
        screen.blit(text, (8, top + index * 23))


def draw_status(
    screen: pygame.Surface,
    game: GameState,
) -> None:
    """Display game status messages."""
    messages = {
        GameStatus.PAUSED: "PAUSED",
        GameStatus.LEVEL_COMPLETE: "LEVEL COMPLETE - Press N",
        GameStatus.GAME_WON: "YOU WIN! - Press R",
        GameStatus.GAME_OVER: "GAME OVER - Press R",
    }

    message = messages.get(game.status)

    if message is None:
        return

    font = pygame.font.Font(None, 36)
    text = font.render(message, True, YELLOW)

    maze_height = len(game.level.maze) * CELL_SIZE

    overlay = pygame.Surface(
        (screen.get_width(), maze_height),
        pygame.SRCALPHA,
    )
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))

    rect = text.get_rect(
        center=(screen.get_width() // 2, maze_height // 2)
    )

    screen.blit(text, rect)


def handle_input(
    event: pygame.event.Event,
    game: GameState,
) -> bool:
    """Forward keyboard commands to GameState."""
    if event.key == pygame.K_ESCAPE:
        return False

    if event.key == pygame.K_r:
        game.restart()
        print("Game restarted")
        return True

    if event.key == pygame.K_p:
        if game.status == GameStatus.PLAYING:
            game.pause()
        elif game.status == GameStatus.PAUSED:
            game.resume()
        return True

    if event.key == pygame.K_n:
        game.next_level()
        return True

    if game.status != GameStatus.PLAYING:
        return True

    direction = KEY_DIRECTIONS.get(event.key)

    if direction is not None:
        game.set_player_direction(direction)

    elif event.key == pygame.K_F1:
        game.toggle_ghost_freeze()
        print("Ghost Freeze:", game.ghosts_frozen)

    elif event.key == pygame.K_F2:
        game.toggle_speed_boost()
        print("Speed Boost:", game.speed_boost)

    elif event.key == pygame.K_F3:
        game.skip_level()
        print("Level skipped")

    return True


def main() -> None:
    """Run the complete engine integration test."""
    config_path = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "config_file.json"
    )

    # 1. Load configuration.
    config = ConfigLoader(config_path).load()

    # 2. Initialize the complete backend.
    game = GameState(config)

    # 3. Initialize pygame.
    pygame.init()

    screen = create_screen(game)
    pygame.display.set_caption(
        "Pac-Man - Complete Engine Test"
    )

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 22)

    print("=== PAC-MAN ENGINE TEST ===")
    print("Configured lives:", config.lives)
    print("Levels:", len(config.levels))
    print("Player speed:", game.player.speed)
    print("Ghosts:", len(game.ghosts))
    print("Press F1/F2/F3 to test cheats")

    running = True
    previous_level = game.level_index
    previous_status = game.status

    while running:
        # 4. Calculate delta time.
        dt = min(clock.tick(FPS) / 1000.0, 0.05)

        # 5. Handle frontend input.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                running = handle_input(event, game)

            if not running:
                break

        if not running:
            break

        # 6. Update the backend.
        game.update(dt)

        # 7. Resize the window if a new level has
        # different dimensions.
        if game.level_index != previous_level:
            screen = create_screen(game)
            previous_level = game.level_index
            print("Now playing level:", previous_level + 1)

        if game.status != previous_status:
            print(
                "Game status:",
                previous_status.name,
                "->",
                game.status.name,
            )
            previous_status = game.status

        # 8. Render the current state.
        screen.fill(BLACK)

        draw_maze(screen, game.level.maze)
        draw_collectibles(screen, game)
        draw_entities(screen, game)
        draw_hud(screen, game, font)
        draw_status(screen, game)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
