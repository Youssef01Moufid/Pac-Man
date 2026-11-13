
from collections import deque
from model.movement import Direction, Movement


class Pathfinder:
    """Find the shortest path between two cells using BFS."""

    def __init__(self, movement: Movement) -> None:
        self.movement = movement

    def find_path(
        self,
        start: tuple[int, int],
        goal: tuple[int, int],
        maze: list[list[int]],
    ) -> list[tuple[int, int]]:
        """Return the shortest path from start to goal."""

        if start == goal:
            return [start]

        queue = deque([start])
        visited = {start}
        parent: dict[
            tuple[int, int],
            tuple[int, int] | None
        ] = {start: None}

        while queue:
            row, col = queue.popleft()

            for direction in Direction:
                neighbor = self.movement.can_move(
                    row, col, maze, direction
                )

                if neighbor is None or neighbor in visited:
                    continue

                visited.add(neighbor)
                parent[neighbor] = (row, col)

                if neighbor == goal:
                    return self._reconstruct_path(parent, goal)

                queue.append(neighbor)

        return []

    def _reconstruct_path(
        self,
        parent: dict[
            tuple[int, int],
            tuple[int, int] | None
        ],
        goal: tuple[int, int],
    ) -> list[tuple[int, int]]:
        """Reconstruct the shortest path using parent cells."""

        path = []
        current: tuple[int, int] | None = goal

        while current is not None:
            path.append(current)
            current = parent[current]

        path.reverse()
        return path
