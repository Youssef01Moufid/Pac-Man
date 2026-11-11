
"""Pygame integration test for the Pac-Man engine."""

import sys

import pygame

from config.loader import ConfigLoader
from game.gamestate import GameState, GameStatus
from model.ghost import Ghost, GhostState, GhostType
from model.movement import Direction


CELL_SIZE = 40
WALL_THICKNESS = 4
HUD_HEIGHT = 155
FPS = 60

COLOR_BG = (0, 0, 0)
COLOR_WALL = (36, 36, 255)
COLOR_PLAYER = (255, 255, 0)
COLOR_PACGUM = (255, 184, 174)
COLOR_SUPER = (255, 255, 255)
COLOR_FRIGHTENED = (40, 90, 255)
COLOR_EATEN = (255, 255, 255)
COLOR_RESPAWNING = (100, 100, 100)
COLOR_TEXT = (235, 235, 235)

GHOST_COLORS = {
    GhostType.RED: (255, 45, 45),
    GhostType.PINK: (255, 130, 190),
    GhostType.CYAN: (0, 225, 235),
    GhostType.ORANGE: (255, 165, 35),
}


def cell_center(
    row: float,
    col: float,
) -> tuple[int, int]:
    """Convert maze coordinates into pixel coordinates."""
    return (
        int((col + 0.5) * CELL_SIZE),
        int((row + 0.5) * CELL_SIZE),
    )


def draw_raw_maze(
    screen: pygame.Surface,
    maze: list[list[int]],
) -> None:
    """Draw maze walls using the raw wall bitmasks."""
    for row, cells in enumerate(maze):
        for col, value in enumerate(cells):
            x = col * CELL_SIZE
            y = row * CELL_SIZE

            if value & 1:
                pygame.draw.line(
                    screen,
                    COLOR_WALL,
                    (x, y),
                    (x + CELL_SIZE, y),
                    WALL_THICKNESS,
                )

            if value & 2:
                pygame.draw.line(
                    screen,
                    COLOR_WALL,
                    (x + CELL_SIZE, y),
                    (x + CELL_SIZE, y + CELL_SIZE),
                    WALL_THICKNESS,
                )

            if value & 4:
                pygame.draw.line(
                    screen,
                    COLOR_WALL,
                    (x, y + CELL_SIZE),
                    (x + CELL_SIZE, y + CELL_SIZE),
                    WALL_THICKNESS,
                )

            if value & 8:
                pygame.draw.line(
                    screen,
                    COLOR_WALL,
                    (x, y),
                    (x, y + CELL_SIZE),
                    WALL_THICKNESS,
                )


def draw_pacgums(
    screen: pygame.Surface,
    positions: set[tuple[int, int]],
) -> None:
    """Draw regular Pac-Gums."""
    for row, col in positions:
        pygame.draw.circle(
            screen,
            COLOR_PACGUM,
            cell_center(row, col),
            max(2, int(CELL_SIZE * 0.1)),
        )


def draw_super_pacgums(
    screen: pygame.Surface,
    positions: set[tuple[int, int]],
) -> None:
    """Draw Super Pac-Gums."""
    for row, col in positions:
        pygame.draw.circle(
            screen,
            COLOR_SUPER,
            cell_center(row, col),
            int(CELL_SIZE * 0.25),
        )


def draw_player(
    screen: pygame.Surface,
    game: GameState,
) -> None:
    """Draw Pac-Man using smooth movement coordinates."""
    if (
        game.invulnerable_remaining > 0.0
        and int(game.invulnerable_remaining * 8) % 2 == 0
    ):
        return

    x, y = game.player.get_world_position()

    pygame.draw.circle(
        screen,
        COLOR_PLAYER,
        cell_center(y, x),
        int(CELL_SIZE * 0.35),
    )


def draw_ghost(
    screen: pygame.Surface,
    ghost: Ghost,
) -> None:
    """Draw a ghost using its type and current state."""
    x, y = ghost.get_world_position()
    cx, cy = cell_center(y, x)

    if ghost.state == GhostState.NORMAL:
        color = GHOST_COLORS[ghost.ghost_type]

    elif ghost.state == GhostState.FRIGHTENED:
        color = COLOR_FRIGHTENED

    elif ghost.state == GhostState.EATEN:
        color = COLOR_EATEN

    else:
        color = COLOR_RESPAWNING

    size = int(CELL_SIZE * 0.65)

    rect = pygame.Rect(0, 0, size, size)
    rect.center = (cx, cy)

    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=7,
    )

    # Draw the ghost's eyes.
    for offset in (-6, 6):
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (cx + offset, cy - 4),
            4,
        )

        pygame.draw.circle(
            screen,
            (20, 20, 20),
            (cx + offset, cy - 4),
            2,
        )


def draw_hud(
    screen: pygame.Surface,
    game: GameState,
    font: pygame.font.Font,
) -> None:
    """Display game information from GameState."""
    maze_height = len(game.level.maze)
    top = maze_height * CELL_SIZE + 8

    lines = [
        (
            f"Level: {game.level_index + 1}/"
            f"{len(game.config.levels)}    "
            f"Score: {game.score}    Lives: {game.lives}"
        ),
        (
            f"Time: {game.time_left:.1f}s    "
            f"Pac-Gums: {len(game.level.pacgums)}    "
            f"Super: {len(game.level.super_pacgums)}"
        ),
        f"Status: {game.status.name}",
    ]

    for index, line in enumerate(lines):
        surface = font.render(
            line,
            True,
            COLOR_TEXT,
        )
        screen.blit(
            surface,
            (10, top + index * 22),
        )

    # Draw four ghost states in two columns.
    ghost_top = top + 70

    for index, ghost in enumerate(game.ghosts):
        state_text = ghost.state.name

        if ghost.state == GhostState.FRIGHTENED:
            state_text += (
                f" {ghost.frightened_remaining:.1f}s"
            )

        elif ghost.state == GhostState.RESPAWNING:
            state_text += (
                f" {ghost.respawn_remaining:.1f}s"
            )

        column = index % 2
        line = index // 2

        x = 10 + column * (screen.get_width() // 2)
        y = ghost_top + line * 23

        label = (
            f"{ghost.ghost_type.name}: {state_text}"
        )

        surface = font.render(
            label,
            True,
            GHOST_COLORS[ghost.ghost_type],
        )

        screen.blit(surface, (x, y))


def draw_status_message(
    screen: pygame.Surface,
    game: GameState,
    font: pygame.font.Font,
) -> None:
    """Display paused and finished game states."""
    messages = {
        GameStatus.PAUSED: "PAUSED - Press P",
        GameStatus.LEVEL_COMPLETE: "LEVEL COMPLETE - Press N",
        GameStatus.GAME_OVER: "GAME OVER - Press R",
        GameStatus.GAME_WON: "YOU WON! - Press R",
    }

    message = messages.get(game.status)

    if message is None:
        return

    maze_height = len(game.level.maze) * CELL_SIZE

    overlay = pygame.Surface(
        (screen.get_width(), maze_height),
        pygame.SRCALPHA,
    )

    overlay.fill((0, 0, 0, 170))
    screen.blit(overlay, (0, 0))

    message_font = pygame.font.Font(None, 34)

    surface = message_font.render(
        message,
        True,
        COLOR_PLAYER,
    )

    rect = surface.get_rect(
        center=(
            screen.get_width() // 2,
            maze_height // 2,
        )
    )

    screen.blit(surface, rect)


def print_controls() -> None:
    """Print test controls in the terminal."""
    print("\n=== PAC-MAN ENGINE TEST ===")
    print("WASD / Arrows : Move Pac-Man")
    print("SPACE         : Frighten ghosts (debug)")
    print("E             : Eat nearest frightened ghost (debug)")
    print("P             : Pause / Resume")
    print("N             : Next level after completion")
    print("C             : Clear collectibles (debug)")
    print("R             : Restart game")
    print("ESC           : Quit")
    print("===========================\n")


def create_window(
    game: GameState,
) -> pygame.Surface:
    """Create or resize the window for the active level."""
    height = len(game.level.maze)
    width = len(game.level.maze[0])

    return pygame.display.set_mode(
        (
            width * CELL_SIZE,
            height * CELL_SIZE + HUD_HEIGHT,
        )
    )


def debug_eat_ghost(game: GameState) -> None:
    """Simulate eating the nearest frightened ghost."""
    edible = [
        ghost
        for ghost in game.ghosts
        if ghost.is_edible
    ]

    if not edible:
        print("No frightened ghost available.")
        return

    px, py = game.player.get_world_position()

    def distance_squared(ghost: Ghost) -> float:
        gx, gy = ghost.get_world_position()
        return (gx - px) ** 2 + (gy - py) ** 2

    nearest = min(edible, key=distance_squared)

    nearest.get_eaten()
    game.score += game.config.points_per_ghost

    print(
        f"DEBUG: {nearest.ghost_type.name} eaten. "
        f"Score: {game.score}"
    )


def handle_keydown(
    event: pygame.event.Event,
    game: GameState,
) -> bool:
    """Process input; return False to quit."""
    if event.key == pygame.K_ESCAPE:
        return False

    if event.key == pygame.K_r:
        game.restart()
        print("Game restarted.")
        print(f"Lives from config: {game.lives}")
        return True

    if event.key == pygame.K_p:
        if game.status == GameStatus.PLAYING:
            game.pause()
            print("Game paused.")

        elif game.status == GameStatus.PAUSED:
            game.resume()
            print("Game resumed.")

        return True

    if event.key == pygame.K_n:
        if game.status == GameStatus.LEVEL_COMPLETE:
            game.next_level()
            print(
                f"Started level {game.level_index + 1}"
            )
        return True

    if game.status != GameStatus.PLAYING:
        return True

    directions = {
        pygame.K_UP: Direction.NORTH,
        pygame.K_w: Direction.NORTH,
        pygame.K_RIGHT: Direction.EAST,
        pygame.K_d: Direction.EAST,
        pygame.K_DOWN: Direction.SOUTH,
        pygame.K_s: Direction.SOUTH,
        pygame.K_LEFT: Direction.WEST,
        pygame.K_a: Direction.WEST,
    }

    direction = directions.get(event.key)

    if direction is not None:
        game.set_player_direction(direction)

    elif event.key == pygame.K_SPACE:
        for ghost in game.ghosts:
            ghost.frightened()

        print("DEBUG: Frightened mode activated.")

    elif event.key == pygame.K_e:
        debug_eat_ghost(game)

    elif event.key == pygame.K_c:
        # Debug only: force the current Level to complete.
        game.level.pacgums.clear()
        game.level.super_pacgums.clear()

        print("DEBUG: All collectibles removed.")

    return True


def main() -> None:
    """Run the full Pac-Man engine integration test."""
    config_path = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "config_file.json"
    )

    # GameState receives the validated configuration.
    config = ConfigLoader(config_path).load()
    game = GameState(config)

    print(f"Config file: {config_path}")
    print(f"Configured lives: {config.lives}")
    print(f"Actual game lives: {game.lives}")
    print(f"Number of levels: {len(config.levels)}")
    print(f"Level time limit: {config.level_max_time}")

    print("\nGhosts:")
    for ghost in game.ghosts:
        print(
            f"{ghost.ghost_type.name}: "
            f"spawn=({ghost.spawn_row}, {ghost.spawn_col})"
        )

    pygame.init()

    screen = create_window(game)
    pygame.display.set_caption(
        "Pac-Man - GameState Integration Test"
    )

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 22)

    print_controls()

    running = True

    previous_level = game.level_index
    previous_status = game.status
    previous_lives = game.lives
    previous_score = game.score

    while running:
        dt = min(clock.tick(FPS) / 1000.0, 0.05)

        # FRONTEND: Process input.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                running = handle_keydown(event, game)

            if not running:
                break

        if not running:
            break

        # BACKEND: Update the complete game simulation.
        game.update(dt)

        # Resize when changing levels with different dimensions.
        if game.level_index != previous_level:
            screen = create_window(game)
            previous_level = game.level_index

        # Print important changes for debugging.
        if game.lives != previous_lives:
            print(f"Lives: {previous_lives} -> {game.lives}")
            previous_lives = game.lives

        if game.score != previous_score:
            print(f"Score: {previous_score} -> {game.score}")
            previous_score = game.score

        if game.status != previous_status:
            print(
                f"Status: {previous_status.name} -> "
                f"{game.status.name}"
            )

            previous_status = game.status

        # FRONTEND: Render current engine state.
        screen.fill(COLOR_BG)

        draw_raw_maze(
            screen,
            game.level.maze,
        )

        draw_pacgums(
            screen,
            game.level.pacgums,
        )

        draw_super_pacgums(
            screen,
            game.level.super_pacgums,
        )

        draw_player(screen, game)

        for ghost in game.ghosts:
            draw_ghost(screen, ghost)

        draw_hud(screen, game, font)
        draw_status_message(screen, game, font)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
