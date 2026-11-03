"""The ghost: an AI entity that chases a target tile through the maze."""

from model.movement import Direction, Movement
from model.entity import Entity

_OPPOSITE: dict[Direction, Direction] = {
    Direction.NORTH: Direction.SOUTH,
    Direction.EAST: Direction.WEST,
    Direction.SOUTH: Direction.NORTH,
    Direction.WEST: Direction.EAST,
}

# The partner's suggested reproducible order for tie-breakers
_TIE_BREAKER_ORDER = [
    Direction.NORTH,
    Direction.EAST,
    Direction.SOUTH,
    Direction.WEST
]


class Ghost(Entity):
    """An AI character that continuously moves toward a target tile."""

    def __init__(self, position: tuple[int, int], speed: float = 3) -> None:
        # Call the parent Entity's __init__
        super().__init__(position, speed)
        
        # The Ghost's brain needs to remember its target during the update loop
        self.target_position: tuple[int, int] | None = None

    def update(
        self,
        dt: float,
        movement: Movement,
        maze: list[list[int]],
        target_position: tuple[int, int],  # Passed in from main.py
    ) -> list[tuple[int, int]]:
        """Save the target, then run the parent Entity's math loop."""
        self.target_position = target_position
        
        return super().update(dt, movement, maze)

    def _choose_direction(
        self,
        movement: Movement,
        maze: list[list[int]],
    ) -> None:
        """Ghost AI: Pick the valid direction that gets us closest to the target."""
        if self.target_position is None:
            return

        row, col = self.position
        target_row, target_col = self.target_position

        possible_directions = list(_TIE_BREAKER_ORDER)

        if self.direction is not None:
            opposite = _OPPOSITE[self.direction]
            if opposite in possible_directions:
                possible_directions.remove(opposite)

        best_direction = None
        shortest_distance = float('inf')

        for d in possible_directions:
            next_cell = movement.can_move(row, col, maze, d)
            
            if next_cell is not None:
                next_r, next_c = next_cell
                
                dist = (target_row - next_r)**2 + (target_col - next_c)**2
                
                if dist < shortest_distance:
                    shortest_distance = dist
                    best_direction = d

        if best_direction is None and self.direction is not None:
            best_direction = _OPPOSITE[self.direction]
            
        self.direction = best_direction