"""Test Pac-Man with four ghosts, collectibles, and collisions."""

import sys
from collections import deque

import pygame

from config.loader import ConfigLoader
from maze.mazegen import MazeGen
from maze.populate import Populate
from model.movement import Direction, Movement
from model.player import Player
from model.ghosts import Ghost, GhostState, GhostType
from model.pathfinder import Pathfinder


CELL_SIZE = 40
WALL_THICKNESS = 4
HUD_HEIGHT = 120
FPS = 60

# Speeds and timers kept exactly as you requested
PLAYER_SPEED = 5.0
GHOST_SPEED = 4.5
FRIGHTENED_TIME = 8.0
RESPAWN_TIME = 3.0
INVULNERABLE_TIME = 1.5
COLLISION_DISTANCE = 0.55

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


def get_reachable_cells(
    maze: list[list[int]],
    movement: Movement,
    start: tuple[int, int],
) -> set[tuple[int, int]]:
    """Return cells reachable from the player's spawn."""
    visited = {start}
    queue = deque([start])

    while queue:
        row, col = queue.popleft()

        for direction in Direction:
            neighbor = movement.can_move(
                row, col, maze, direction
            )

            if neighbor is None or neighbor in visited:
                continue

            visited.add(neighbor)
            queue.append(neighbor)

    return visited


def choose_corner_positions(
    available: set[tuple[int, int]],
    corners: list[tuple[int, int]],
    preferred: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    """Select distinct reachable positions near the corners."""
    candidates = set(available)
    result = []

    for index, corner in enumerate(corners):
        if not candidates:
            break

        preferred_cell = (
            preferred[index]
            if index < len(preferred)
            else corner
        )

        if preferred_cell in candidates:
            selected = preferred_cell
        else:
            selected = min(
                candidates,
                key=lambda cell: (
                    abs(cell[0] - corner[0])
                    + abs(cell[1] - corner[1]),
                    cell[0],
                    cell[1],
                ),
            )

        result.append(selected)
        candidates.remove(selected)

    return result


def cell_center(
    row: float,
    col: float,
) -> tuple[int, int]:
    """Convert maze cell coordinates into pixel coordinates."""
    return (
        int((col + 0.5) * CELL_SIZE),
        int((row + 0.5) * CELL_SIZE),
    )


def draw_raw_maze(
    screen: pygame.Surface,
    maze: list[list[int]],
) -> None:
    """Draw the maze using its wall bitmasks."""
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
    """Draw normal Pac-Gums."""
    for row, col in positions:
        pygame.draw.circle(
            screen,
            COLOR_PACGUM,
            cell_center(row, col),
            int(CELL_SIZE * 0.1),
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
    player: Player,
    invulnerable_remaining: float,
) -> None:
    """Draw Pac-Man with smooth movement."""
    if (
        invulnerable_remaining > 0.0
        and int(invulnerable_remaining * 8) % 2 == 0
    ):
        return

    x, y = player.get_world_position()

    pygame.draw.circle(
        screen,
        COLOR_PLAYER,
        cell_center(y, x),
        int(CELL_SIZE * 0.35),
    )


def draw_ghost(
    screen: pygame.Surface,
    ghost_type: GhostType,
    ghost: Ghost,
) -> None:
    """Draw a ghost according to its type and state."""
    x, y = ghost.get_world_position()
    cx, cy = cell_center(y, x)

    if ghost.state == GhostState.NORMAL:
        color = GHOST_COLORS[ghost_type]
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
        screen, color, rect, border_radius=7
    )

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
    font: pygame.font.Font,
    ghosts: list[tuple[GhostType, Ghost]],
    maze_height: int,
    score: int,
    lives: int,
    pacgum_count: int,
    super_count: int,
    game_status: str | None,
) -> None:
    """Display score, lives, and ghost states."""
    top = maze_height * CELL_SIZE + 5

    status = (
        f"Score: {score}   Lives: {lives}   "
        f"Pac-Gums: {pacgum_count}   Super: {super_count}"
    )

    screen.blit(
        font.render(status, True, COLOR_TEXT),
        (10, top),
    )

    for index, (ghost_type, ghost) in enumerate(ghosts):
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
        y = top + 25 + line * 22

        label = f"{ghost_type.name}: {state_text}"

        screen.blit(
            font.render(
                label, True, GHOST_COLORS[ghost_type]
            ),
            (x, y),
        )

    controls = "Arrows/WASD: Move  SPACE: Frighten  E: Eat  R: Reset"

    screen.blit(
        font.render(controls, True, COLOR_TEXT),
        (10, top + 75),
    )

    # FIXED SYNTAX ERROR HERE
    if game_status is not None:
        message = font.render(
            f"{game_status} - Press R to restart",
            True,
            (255, 80, 80),
        )

        rect = message.get_rect(
            center=(
                screen.get_width() // 2,
                maze_height * CELL_SIZE // 2,
            )
        )

        screen.blit(message, rect)


def ghosts_collide(
    player: Player,
    ghost: Ghost,
) -> bool:
    """Check collisions using smooth world positions."""
    px, py = player.get_world_position()
    gx, gy = ghost.get_world_position()

    distance_squared = (
        (px - gx) ** 2 + (py - gy) ** 2
    )

    return distance_squared <= COLLISION_DISTANCE ** 2


def main() -> None:
    """Run the complete Pac-Man ghost test."""
    config_path = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "config_file.json"
    )

    # Read configuration.
    config = ConfigLoader(config_path).load()
    level_cfg = config.levels[0]

    print(f"Configuration: {config_path}")
    print(f"Configured lives: {config.lives}")
    print(f"Level width: {level_cfg.width}")
    print(f"Level height: {level_cfg.height}")
    print(f"Pac-Gums requested: {level_cfg.pacgum}")

    # Generate maze.
    maze = MazeGen(
        width=level_cfg.width,
        height=level_cfg.height,
    ).generate(seed=config.seed)

    populate = Populate(
        maze,
        level_cfg.width,
        level_cfg.height,
        level_cfg.pacgum,
    )

    # Initialize movement systems.
    movement = Movement()
    pathfinder = Pathfinder(movement)

    player_spawn = populate.find_player_spawn()

    player = Player(
        row=player_spawn[0],
        col=player_spawn[1],
        speed=PLAYER_SPEED,
    )

    # Find all cells reachable by Pac-Man.
    reachable = get_reachable_cells(
        maze, movement, player_spawn
    )

    height = len(maze)
    width = len(maze[0])

    corners = [
        (0, 0),
        (0, width - 1),
        (height - 1, 0),
        (height - 1, width - 1),
    ]

    # Choose four accessible spawn positions.
    ghost_spawns = choose_corner_positions(
        available=reachable - {player_spawn},
        corners=corners,
        preferred=populate.find_ghosts_spawn(),
    )

    if len(ghost_spawns) != 4:
        raise ValueError(
            "Not enough reachable cells for four ghosts."
        )

    ghost_types = [
        GhostType.RED,
        GhostType.PINK,
        GhostType.CYAN,
        GhostType.ORANGE,
    ]

    ghosts: list[tuple[GhostType, Ghost]] = []

    # Create four ghosts with their individual types.
    for ghost_type, (row, col) in zip(
        ghost_types, ghost_spawns
    ):
        ghost = Ghost(
            row=row,
            col=col,
            speed=GHOST_SPEED,
            frightened_timer=FRIGHTENED_TIME,
            respawn_timer=RESPAWN_TIME,
            pathfinder=pathfinder,
            ghost_type=ghost_type,
        )

        ghosts.append((ghost_type, ghost))

        print(
            f"{ghost_type.name} spawn: ({row}, {col})"
        )

    # Generate collectibles once.
    reserved = {player_spawn, *ghost_spawns}

    super_positions = set(
        choose_corner_positions(
            available=reachable - reserved,
            corners=corners,
            preferred=populate.find_superpacgum_spawn(),
        )
    )

    pacgum_positions = set(
        populate.find_pacgum_spawn()
    )

    pacgum_positions &= reachable
    pacgum_positions -= reserved
    pacgum_positions -= super_positions

    initial_pacgums = pacgum_positions.copy()
    initial_supers = super_positions.copy()

    pygame.init()

    screen = pygame.display.set_mode(
        (
            width * CELL_SIZE,
            height * CELL_SIZE + HUD_HEIGHT,
        )
    )

    pygame.display.set_caption(
        "Pac-Man - Four Ghost AI Test"
    )

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 22)

    # Use the number of lives from the config file.
    score = 0
    lives = config.lives
    game_status: str | None = None
    invulnerable_remaining = 0.0

    print("\nCONTROLS")
    print("WASD / Arrows: Move Pac-Man")
    print("SPACE: Make all ghosts frightened")
    print("E: Eat nearest frightened ghost (debug)")
    print("R: Restart game")
    print("ESC: Quit\n")

    running = True

    while running:
        dt = min(clock.tick(FPS) / 1000.0, 0.05)

        # Handle keyboard input.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_r:
                    player.reset()

                    for _, ghost in ghosts:
                        ghost.reset()

                    pacgum_positions = initial_pacgums.copy()
                    super_positions = initial_supers.copy()

                    score = 0
                    lives = config.lives
                    game_status = None
                    invulnerable_remaining = 0.0

                    print("Game restarted!")
                    print(f"Lives restored: {lives}")

                elif game_status is None:
                    if event.key in (
                        pygame.K_UP, pygame.K_w
                    ):
                        player.set_direction(Direction.NORTH)

                    elif event.key in (
                        pygame.K_DOWN, pygame.K_s
                    ):
                        player.set_direction(Direction.SOUTH)

                    elif event.key in (
                        pygame.K_LEFT, pygame.K_a
                    ):
                        player.set_direction(Direction.WEST)

                    elif event.key in (
                        pygame.K_RIGHT, pygame.K_d
                    ):
                        player.set_direction(Direction.EAST)

                    elif event.key == pygame.K_SPACE:
                        print("DEBUG: Frightened mode!")

                        for _, ghost in ghosts:
                            ghost.frightened()

                    elif event.key == pygame.K_e:
                        edible_ghosts = [
                            ghost
                            for _, ghost in ghosts
                            if ghost.is_edible
                        ]

                        if edible_ghosts:
                            px, py = player.get_world_position()

                            nearest = min(
                                edible_ghosts,
                                key=lambda ghost: (
                                    (
                                        ghost.get_world_position()[0]
                                        - px
                                    ) ** 2
                                    + (
                                        ghost.get_world_position()[1]
                                        - py
                                    ) ** 2
                                ),
                            )

                            nearest.get_eaten()
                            score += config.points_per_ghost

                            print(
                                "DEBUG: Ghost eaten! "
                                "Returning to spawn."
                            )

        if not running:
            break

        if game_status is None:
            invulnerable_remaining = max(
                0.0, invulnerable_remaining - dt
            )

            # Update Pac-Man.
            arrived = player.update(
                dt, movement, maze
            )

            visited_cells = [
                (player.row, player.col),
                *arrived,
            ]

            # Eat normal and Super Pac-Gums.
            for position in visited_cells:
                if position in pacgum_positions:
                    pacgum_positions.remove(position)
                    score += config.points_per_pacgum

                    print(
                        f"Pac-Gum eaten! Score: {score}"
                    )

                if position in super_positions:
                    super_positions.remove(position)
                    score += config.points_per_super_pacgum

                    print("SUPER PAC-GUM EATEN!")

                    for _, ghost in ghosts:
                        ghost.frightened()

            # Update all four ghosts.
            for ghost_type, ghost in ghosts:
                previous_state = ghost.state

                ghost.set_target(
                    player.row, player.col
                )

                ghost.update(dt, movement, maze)

                if ghost.state != previous_state:
                    print(
                        f"{ghost_type.name}: "
                        f"{previous_state.name} -> "
                        f"{ghost.state.name}"
                    )

            # Check ghost collisions.
            if invulnerable_remaining <= 0.0:
                dangerous_collision = any(
                    ghost.is_dangerous
                    and ghosts_collide(player, ghost)
                    for _, ghost in ghosts
                )

                if dangerous_collision:
                    lives -= 1

                    print(
                        f"Pac-Man hit! Lives: {lives}"
                    )

                    player.reset()

                    for _, ghost in ghosts:
                        ghost.reset()

                    invulnerable_remaining = (
                        INVULNERABLE_TIME
                    )

                    if lives <= 0:
                        game_status = "GAME OVER"
                        print("GAME OVER!")

                else:
                    for ghost_type, ghost in ghosts:
                        if (
                            ghost.is_edible
                            and ghosts_collide(player, ghost)
                        ):
                            ghost.get_eaten()
                            score += config.points_per_ghost

                            print(
                                f"{ghost_type.name} EATEN! "
                                f"Score: {score}"
                            )

            # Check level completion.
            if (
                game_status is None
                and not pacgum_positions
                and not super_positions
            ):
                game_status = "LEVEL COMPLETE"
                print(
                    f"LEVEL COMPLETE! Score: {score}"
                )

        # Draw frame.
        screen.fill(COLOR_BG)

        draw_raw_maze(screen, maze)

        draw_pacgums(
            screen, pacgum_positions
        )

        draw_super_pacgums(
            screen, super_positions
        )

        draw_player(
            screen, player, invulnerable_remaining
        )

        for ghost_type, ghost in ghosts:
            draw_ghost(
                screen, ghost_type, ghost
            )

        draw_hud(
            screen=screen,
            font=font,
            ghosts=ghosts,
            maze_height=height,
            score=score,
            lives=lives,
            pacgum_count=len(pacgum_positions),
            super_count=len(super_positions),
            game_status=game_status,
        )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()