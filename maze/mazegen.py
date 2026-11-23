
"""Provide a wrapper for generating Pac-Man mazes."""

from mazegenerator.mazegenerator import MazeGenerator
from typing import cast


class MazeGen:
    """Generate mazes using the external MazeGenerator package.

    Store the requested maze dimensions and provide a method
    to generate a two-dimensional maze represented by integers.
    """

    def __init__(self, width: int, height: int) -> None:
        """Initialize the maze generator with the requested dimensions.

        Args:
            width: Number of cells in the maze horizontally.
            height: Number of cells in the maze vertically.
        """

        self.width = width
        self.height = height

    def _get_dim(self) -> tuple[int, int]:
        """Return the configured maze dimensions.

        Returns:
            A tuple containing the maze width and height.
        """
        return self.width, self.height

    def generate(self, seed: int) -> list[list[int]]:
        """Generate a maze using the configured dimensions and seed.

        Create a MazeGenerator instance with perfect mode disabled.
        The generated maze is represented as a two-dimensional
        list of integers, where each integer encodes cell walls.

        Args:
            seed: Seed passed to the external maze generator.
                A fixed seed produces reproducible generation,
                while seed 0 requests random generation.

        Returns:
            A two-dimensional list of integers representing
            the generated maze.
        """
        size = self._get_dim()
        generator = MazeGenerator(size=size, perfect=False, seed=seed)
        return cast(list[list[int]], generator.maze)
