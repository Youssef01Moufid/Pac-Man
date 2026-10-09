from mazegenerator.mazegenerator import MazeGenerator


def render(maze: list[list[int]]) -> str:
    """Draws the maze as (2h+1) x (2w+1) tiles: '#' wall, ' ' floor."""
    h, w = len(maze), len(maze[0])
    tiles = [["+"] * (2 * w + 1) for _ in range(2 * h + 1)]
    for y in range(h):
        for x in range(w):
            v = maze[y][x]
            if v == 15:
                continue
            tiles[2 * y + 1][2 * x + 1] = " "
            if not v & 2 and x + 1 < w:
                tiles[2 * y + 1][2 * x + 2] = " "
            if not v & 4 and y + 1 < h:
                tiles[2 * y + 2][2 * x + 1] = " "
    return "\n".join("".join(row) for row in tiles)


small = MazeGenerator(size=(5, 5), perfect=False, seed=42)
print("raw 5x5 (row y, column x):")
for row in small.maze:
    print(row)

big = MazeGenerator(size=(15, 15), perfect=False, seed=42)
print("\n15x15 rendered:")
print(render(big.maze))

same = MazeGenerator(size=(15, 15), perfect=False, seed=42)
print("\nsame seed gives same maze:", big.maze == same.maze)

a = MazeGenerator(size=(15, 15), perfect=False, seed=0)
b = MazeGenerator(size=(15, 15), perfect=False, seed=0)
print("seed=0 reproducible:", a.maze == b.maze)