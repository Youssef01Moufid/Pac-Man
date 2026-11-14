
"""Coordinate Pac-Man game rules and level progression."""

from enum import Enum, auto
from typing import Any

from maze.mazegen import MazeGen
from maze.populate import Populate
from model.ghost import Ghost, GhostType
from game.level import CollectibleType, Level
from model.movement import Direction, Movement
from model.pathfinder import Pathfinder
from model.player import Player


PLAYER_SPEED = 5.0
GHOST_SPEED = 4.5
FRIGHTENED_TIME = 8.0
RESPAWN_TIME = 3.0
INVULNERABLE_TIME = 1.5
COLLISION_DISTANCE = 0.55


class GameStatus(Enum):
    """Possible states of the game."""

    PLAYING = auto()
    PAUSED = auto()
    LEVEL_COMPLETE = auto()
    GAME_OVER = auto()
    GAME_WON = auto()


class GameState:
    """Manage the current level, entities, and game rules."""

    def __init__(self, config: Any) -> None:
        """Initialize the game using validated configuration."""
        self.config = config

        self.movement = Movement()
        self.pathfinder = Pathfinder(self.movement)

        self.level_index = 0
        self.score = 0
        self.lives = config.lives

        self.time_left = 0.0
        self.invulnerable_remaining = 0.0

        self.status = GameStatus.PLAYING

        self._setup_level()

    def _setup_level(self) -> None:
        """Generate and populate the current level."""
        level_config = self.config.levels[self.level_index]

        seed = self.config.seed if self.level_index == 0 else 0

        maze = MazeGen(
            width=level_config.width,
            height=level_config.height,
        ).generate(seed=seed)

        populate = Populate(
            maze,
            level_config.width,
            level_config.height,
            level_config.pacgum,
        )

        player_spawn = populate.find_player_spawn()
        ghost_spawns = populate.find_ghosts_spawn()
        pacgums = set(populate.find_pacgum_spawn())
        super_pacgums = set(
            populate.find_superpacgum_spawn()
        )

        self.level = Level(
            maze=maze,
            pacgums=pacgums,
            super_pacgums=super_pacgums,
        )

        self.player = Player(
            row=player_spawn[0],
            col=player_spawn[1],
            speed=PLAYER_SPEED,
        )

        ghost_types = [
            GhostType.RED,
            GhostType.PINK,
            GhostType.CYAN,
            GhostType.ORANGE,
        ]

        self.ghosts: list[Ghost] = []

        for ghost_type, (row, col) in zip(
            ghost_types, ghost_spawns
        ):
            ghost = Ghost(
                row=row,
                col=col,
                speed=GHOST_SPEED,
                frightened_timer=FRIGHTENED_TIME,
                respawn_timer=RESPAWN_TIME,
                pathfinder=self.pathfinder,
                ghost_type=ghost_type,
            )

            self.ghosts.append(ghost)

        self.time_left = float(self.config.level_max_time)
        self.invulnerable_remaining = 0.0
        self.status = GameStatus.PLAYING

    def set_player_direction(
        self,
        direction: Direction,
    ) -> None:
        """Forward movement input to Pac-Man."""
        if self.status == GameStatus.PLAYING:
            self.player.set_direction(direction)

    def _handle_collectibles(
        self,
        positions: list[tuple[int, int]],
    ) -> None:
        """Apply the effects of collected Pac-Gums."""
        for position in positions:
            collectible = self.level.eat_at(position)

            if collectible == CollectibleType.PACGUM:
                self.score += self.config.points_per_pacgum

            elif collectible == CollectibleType.SUPER_PACGUM:
                self.score += (
                    self.config.points_per_super_pacgum
                )

                for ghost in self.ghosts:
                    ghost.frightened()

    def _collides_with(self, ghost: Ghost) -> bool:
        """Check the distance between Pac-Man and a ghost."""
        player_x, player_y = (
            self.player.get_world_position()
        )

        ghost_x, ghost_y = ghost.get_world_position()

        distance_squared = (
            (player_x - ghost_x) ** 2
            + (player_y - ghost_y) ** 2
        )

        return distance_squared <= COLLISION_DISTANCE ** 2

    def _handle_collisions(self) -> None:
        """Handle dangerous and edible ghost collisions."""
        if self.invulnerable_remaining > 0.0:
            return

        for ghost in self.ghosts:
            if ghost.is_dangerous and self._collides_with(ghost):
                self._lose_life()
                return

        for ghost in self.ghosts:
            if ghost.is_edible and self._collides_with(ghost):
                ghost.get_eaten()
                self.score += self.config.points_per_ghost

    def _lose_life(self) -> None:
        """Remove one life and reset character positions."""
        self.lives -= 1

        if self.lives <= 0:
            self.lives = 0
            self.status = GameStatus.GAME_OVER
            return

        self.player.reset()

        for ghost in self.ghosts:
            ghost.reset()

        self.invulnerable_remaining = INVULNERABLE_TIME

    def _handle_timeout(self) -> None:
        """Apply the time-up rule."""
        self._lose_life()

        if self.status == GameStatus.PLAYING:
            self.time_left = float(
                self.config.level_max_time
            )

    def _check_level_completion(self) -> None:
        """Check whether the current level is finished."""
        if not self.level.is_complete():
            return

        if self.level_index == len(self.config.levels) - 1:
            self.status = GameStatus.GAME_WON
        else:
            self.status = GameStatus.LEVEL_COMPLETE

    def update(self, dt: float) -> None:
        """Advance one frame of game simulation."""
        if self.status != GameStatus.PLAYING:
            return

        if dt <= 0.0:
            return

        self.time_left = max(
            0.0, self.time_left - dt
        )

        if self.time_left <= 0.0:
            self._handle_timeout()
            return

        self.invulnerable_remaining = max(
            0.0,
            self.invulnerable_remaining - dt,
        )

        arrived = self.player.update(
            dt, self.movement, self.level.maze
        )

        visited_positions = [
            *arrived,
            (self.player.row, self.player.col),
        ]

        self._handle_collectibles(visited_positions)

        for ghost in self.ghosts:
            ghost.set_target(
                self.player.row,
                self.player.col,
            )

            ghost.update(
                dt, self.movement, self.level.maze
            )

        self._handle_collisions()

        if self.status != GameStatus.PLAYING:
            return

        self._check_level_completion()

    def next_level(self) -> None:
        """Advance to the next configured level."""
        if self.status != GameStatus.LEVEL_COMPLETE:
            return

        if self.level_index + 1 >= len(self.config.levels):
            self.status = GameStatus.GAME_WON
            return

        self.level_index += 1
        self._setup_level()

    def pause(self) -> None:
        """Pause the game."""
        if self.status == GameStatus.PLAYING:
            self.status = GameStatus.PAUSED

    def resume(self) -> None:
        """Resume a paused game."""
        if self.status == GameStatus.PAUSED:
            self.status = GameStatus.PLAYING

    def restart(self) -> None:
        """Restart the entire game from the first level."""
        self.level_index = 0
        self.score = 0
        self.lives = self.config.lives

        self._setup_level()
