"""Draw every level of a config as a picture and open it in the browser.

Writes maze_preview.html in the current folder.
Run from the project root:  python3 maze_preview.py config_file.json
"""

import sys
import webbrowser
from pathlib import Path

from config.loader import ConfigLoader
from maze.adapter import MazeAdapter
from maze.grid import TileGrid

TILE = 14  # pixels per tile
WALL_COLOR = "#2a3cd0"
FLOOR_COLOR = "#05050f"
OUTPUT = Path("maze_preview.html")

PAGE_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Pac-Man maze preview</title>
<style>
body { background: #111; color: #ddd; font-family: sans-serif; margin: 24px; }
h1 { font-size: 22px; }
h2 { font-size: 16px; margin: 28px 0 4px; }
p { margin: 0 0 8px; color: #999; font-size: 13px; }
svg { max-width: 100%; height: auto; }
</style>
</head>
<body>
<h1>Pac-Man maze preview</h1>
"""

PAGE_TAIL = "\n</body>\n</html>\n"


def grid_to_svg(grid: TileGrid) -> str:
    """Return an <svg> picture of the grid: blue walls, black corridors."""
    runs = []
    for row in range(grid.height):
        col = 0
        while col < grid.width:
            if not grid.is_floor(row, col):
                col += 1
                continue
            start = col
            while col < grid.width and grid.is_floor(row, col):
                col += 1
            length = col - start
            runs.append(f"M{start} {row}h{length}v1h-{length}z")
    path_data = "".join(runs)
    return (
        f'<svg viewBox="0 0 {grid.width} {grid.height}" '
        f'width="{grid.width * TILE}" height="{grid.height * TILE}" '
        'shape-rendering="crispEdges" xmlns="http://www.w3.org/2000/svg">'
        f'<rect width="{grid.width}" height="{grid.height}" '
        f'fill="{WALL_COLOR}"/>'
        f'<path d="{path_data}" fill="{FLOOR_COLOR}"/>'
        "</svg>"
    )


def main() -> int:
    """Build every level from the config and write the preview page."""
    if len(sys.argv) != 2:
        print("Usage: python3 maze_preview.py <config.json>")
        return 1

    config = ConfigLoader(sys.argv[1]).load()
    sections = []
    for index, level in enumerate(config.levels):
        seed = config.seed if index == 0 else 0
        grid = MazeAdapter(level.width, level.height).generate(seed)
        kind = f"fixed seed {seed}" if index == 0 else "random"
        sections.append(
            f"<h2>Level {index + 1}</h2>"
            f"<p>asked {level.width}x{level.height}, "
            f"got {grid.width}x{grid.height}, {kind}</p>"
            f"{grid_to_svg(grid)}"
        )

    page = PAGE_HEAD + "\n".join(sections) + PAGE_TAIL
    try:
        OUTPUT.write_text(page, encoding="utf-8")
    except OSError as err:
        print(f"Could not write {OUTPUT}: {err}")
        return 1

    print(f"Wrote {OUTPUT.resolve()}")
    webbrowser.open(OUTPUT.resolve().as_uri())
    return 0


if __name__ == "__main__":
    sys.exit(main())
