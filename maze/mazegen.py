from mazegenerator.mazegenerator import MazeGenerator


class MazeGen:

    def __init__(self, width: int, height: int) -> None:

        self.width = width
        self.height = height

    def _get_dim(self) -> tuple[int, int]:
        return self.width, self.height

    def generate(self, seed: int) -> list[list[int]]:
        size = self._get_dim()
        generator = MazeGenerator(size=size, perfect=False, seed=seed)
        return generator.maze
