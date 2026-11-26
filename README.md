# Pac-Man — 42 Project

*This project has been created as part of the 42 curriculum by **ymoufid** and **ichokair**.*

## Description

Pac-Man is a maze-based arcade game developed in **Python using Pygame**.

The objective is to navigate through procedurally generated mazes, collect Pac-Gums and Super Pac-Gums, avoid dangerous ghosts, and complete all levels while earning the highest possible score.

The game includes:

- Procedurally generated mazes using the assigned **A-Maze-ing** package.
- At least 10 configurable levels.
- Four ghosts with different movement behaviors.
- Smooth, frame-rate-independent character movement.
- Regular Pac-Gums and Super Pac-Gums.
- Ghost frightened, eaten, and respawning states.
- Scoring, lives, and per-level timers.
- Three cheat features: Ghost Freeze, Speed Boost, and Level Skip.
- JSON-based configuration with validation and fallback values.

The first level uses a fixed seed to generate a reproducible maze. Subsequent levels are randomly generated.

---

## Instructions

### Requirements

To run the game from source:

- Python 3.13
- `uv` package manager
- Pygame
- The assigned A-Maze-ing package

Dependencies are managed through `pyproject.toml` and `uv.lock`.

The packaged Linux application does not require users to install Python or Pygame separately.

### Installation

Clone the repository:

```bash
git clone https://github.com/Youssef01Moufid/Pac-Man.git
cd Pac-Man
```

Install the project dependencies:

```bash
uv sync
```

### Execution

Run the game using:

```bash
uv run python pac-man.py config_file.json
```

Alternatively, use the Makefile:

```bash
make run
```

### Controls

| Key | Action |
|---|---|
| W / Up arrow | Move north |
| S / Down arrow | Move south |
| A / Left arrow | Move west |
| D / Right arrow | Move east |
| P | Pause / Resume |
| R | Restart the game |
| ESC | Quit |

### Cheat Mode

Cheat mode is intended to facilitate peer evaluation and testing.

| Key | Feature | Description |
|---|---|---|
| F1 | Ghost Freeze | Freeze or unfreeze ghost movement |
| F2 | Speed Boost | Increase or restore Pac-Man's speed |
| F3 | Level Skip | Immediately complete the current level |
| N | Next Level | Continue after level completion |

*These keys reflect the engine test controls. Verify them against the final frontend before submission.*

### Game Rules

- Pac-Man starts near the center of the maze.
- Four ghosts start in the four corners.
- Regular Pac-Gums increase the score.
- Super Pac-Gums temporarily make eligible ghosts frightened.
- Frightened ghosts can be eaten for additional points.
- Touching a normal ghost costs one life.
- When Pac-Man loses a life, characters return to their spawn positions.
- Collected Pac-Gums remain collected after losing a life.
- A level is completed when all regular and Super Pac-Gums have been collected.
- Score and remaining lives are preserved between levels.
- The game ends when all lives are lost or all levels are completed.

---

## Configuration

The game uses a JSON configuration file, typically named `config_file.json`.

The configuration is loaded through `ConfigLoader`, which validates input values and applies defaults when necessary.

### Global Configuration

| Parameter | Description | Default |
|---|---|---|
| `highscore_filename` | File used to store highscores | `highscores.json` |
| `lives` | Initial number of lives | 3 |
| `points_per_pacgum` | Points for a regular Pac-Gum | 10 |
| `points_per_super_pacgum` | Points for a Super Pac-Gum | 50 |
| `points_per_ghost` | Points for eating a frightened ghost | 200 |
| `seed` | Seed used for the first level | 42 |
| `levels` | List of level configurations | 10 default levels |

### Per-Level Configuration

Each level has its own parameters.

| Parameter | Description | Default |
|---|---|---|
| `width` | Maze width, odd integer between 9 and 51 | 21 |
| `height` | Maze height, odd integer between 9 and 51 | 21 |
| `pacgum` | Requested number of regular Pac-Gums | 42 |
| `level_max_time` | Time limit in seconds, between 10 and 600 | 90 |

### Configuration Example

```json
{
    "highscore_filename": "highscores.json",
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "levels": [
        {
            "width": 21,
            "height": 21,
            "pacgum": 42,
            "level_max_time": 120
        },
        {
            "width": 25,
            "height": 25,
            "pacgum": 60,
            "level_max_time": 90
        }
    ]
}
```

The example defines two levels. `ConfigLoader` automatically adds default levels until the minimum of 10 is reached.

The loader also supports `#` comments in configuration files, validates data types, and records warnings for invalid values.

---

## Highscore System

The game configuration defines the highscore file through `highscore_filename`.

The highscore system is intended to record player scores and allow comparison between game sessions.

The configuration supports filenames and relative paths such as:

```json
{
    "highscore_filename": "./test/highscores.json"
}
```

The highscore storage implementation is responsible for creating missing parent directories and saving score data.

The highscore file is runtime data and should not be confused with the configuration file.

---

## Maze Generation

Mazes are generated using the assigned **A-Maze-ing** package.

The game uses a `MazeGen` wrapper to request maze generation according to the current level configuration.

### Maze Representation

Each generated maze is represented as a two-dimensional list of integers.

Each integer contains a bitmask describing the walls surrounding a cell.

| Direction | Bit value |
|---|---|
| North | 1 |
| East | 2 |
| South | 4 |
| West | 8 |

For example:

- `15` represents a cell with all four walls closed.
- `0` represents a cell without surrounding walls.

Movement and rendering interpret these wall bitmasks to determine passages and draw the maze.

### Level Generation

The game applies the following seed policy:

- **Level 1:** Uses the fixed seed specified by the configuration.
- **Levels 2 onward:** Use random generation with seed `0` according to the generator's interface.

The `Populate` class determines the initial positions of Pac-Man, ghosts, and collectibles.

Pac-Man is placed near the center of the maze. The four ghosts and Super Pac-Gums are placed in the corners.

Regular Pac-Gums are placed in available cells without overlapping reserved spawn positions.

---

## Implementation

The project separates game logic, movement, maze generation, configuration, and rendering into dedicated components.

### Movement System

The `Movement` class validates movement between neighboring maze cells using wall bitmasks.

The `Entity` class provides shared smooth movement functionality for Pac-Man and ghosts.

Movement uses:

- Logical cell coordinates (`row`, `col`).
- Direction.
- Movement speed in cells per second.
- Progress between neighboring cell centers.
- Delta time (`dt`) for frame-rate-independent movement.

### Player

The `Player` class inherits movement behavior from `Entity`.

It responds to directional input and reports the cells reached during movement, allowing the game engine to process collectible consumption.

### Ghost AI

The game has four types of ghosts:

| Ghost | Normal behavior |
|---|---|
| Red | Chases Pac-Man using BFS |
| Pink | Random movement |
| Cyan | Random movement |
| Orange | Combines chasing and random movement based on distance |

Each ghost uses a state machine with four states:

- `NORMAL`: Standard movement behavior.
- `FRIGHTENED`: Attempts to move away from Pac-Man.
- `EATEN`: Returns toward its spawn using pathfinding.
- `RESPAWNING`: Waits before returning to normal behavior.

The `Pathfinder` class uses Breadth-First Search (BFS) to determine shortest paths through the maze.

### Game Management

The `GameState` class coordinates the game engine.

Its main responsibilities include:

- Initializing levels and entities.
- Updating Player and Ghost objects.
- Processing Pac-Gum collection.
- Applying scoring rules.
- Detecting ghost collisions.
- Managing lives and temporary invulnerability.
- Handling per-level timers.
- Managing pause, victory, and game-over states.
- Handling level progression.
- Applying cheat features.

The `Level` class stores the current maze and remaining collectibles, providing methods to consume items and detect level completion.

---

## General Software Architecture

The project uses a modular architecture with a clear separation of responsibilities.

```text
Frontend (Pygame)
       |
       v
    GameState
       |
       +---- Level
       |       |
       |       +---- Maze
       |       +---- Pac-Gums
       |       +---- Super Pac-Gums
       |
       +---- Player
       |
       +---- Ghosts
       |       |
       |       +---- Pathfinder (BFS)
       |
       +---- Movement
       |
       +---- MazeGen
       |
       +---- Populate

ConfigLoader ---> Config ---> GameState
```

### Main Components

| Component | Responsibility |
|---|---|
| `ConfigLoader` | Load and validate JSON configuration |
| `DefaultsSchema` | Define default values and validation rules |
| `MazeGen` | Generate mazes |
| `Populate` | Calculate initial positions |
| `Movement` | Validate movement between cells |
| `Pathfinder` | Calculate shortest paths |
| `Entity` | Provide shared smooth movement |
| `Player` | Represent Pac-Man |
| `Ghost` | Implement ghost states and AI |
| `Level` | Manage the maze and collectibles |
| `GameState` | Coordinate gameplay and level progression |
| Frontend | Display the game and process user input |

### Backend–Frontend Communication

`GameState` serves as the main interface between the engine and the frontend.

The frontend advances the simulation using:

```python
game.update(dt)
```

It can obtain Pac-Man's smooth position using:

```python
x, y = game.player.get_world_position()
```

Ghost positions are accessed similarly:

```python
for ghost in game.ghosts:
    x, y = ghost.get_world_position()
```

The frontend can also read score, lives, remaining time, level data, and game status.

This keeps rendering separate from gameplay rules.

---

## Project Packaging and Deployment

The project uses **PyInstaller** to package the Python/Pygame game into a standalone Linux executable.

The packaged version is intended to be distributed through **itch.io**, allowing reviewers to download and launch the game without installing Python or Pygame.

### 1. Packaging Requirements

The build environment requires:

- Linux (64-bit).
- Python 3.13.
- `uv` package manager.
- GNU Make.
- PyInstaller and the project dependencies.

Install dependencies with:

```bash
uv sync
```

### 2. Build the Executable

The repository contains a `Makefile` with a `build` target.

From the project root, run:

```bash
make build
```

The build uses the following PyInstaller command:

```bash
uv run pyinstaller --onefile --name pac-man \
    --add-data "assets:assets" \
    --add-data "config_file.json:." \
    pac-man.py
```

**Explanation of the options:**

| Option | Description |
|---|---|
| `--onefile` | Package the game into a single executable |
| `--name pac-man` | Name the executable `pac-man` |
| `--add-data "assets:assets"` | Include fonts, images, and game assets |
| `--add-data "config_file.json:."` | Include a default configuration file in the bundle |
| `pac-man.py` | Main game entry point |

PyInstaller packages the Python runtime and required application dependencies.

The generated executable targets the Linux environment in which it is built. A separate build is required for Windows or other operating systems.

### 3. Generated Files

After successfully running `make build`, PyInstaller generates:

```text
pac-man/
├── build/
│   └── pac-man/
├── dist/
│   └── pac-man
├── pac-man.spec
├── pac-man.py
└── Makefile
```

- `build/`: Temporary analysis and intermediate packaging files.
- `dist/`: Contains the generated executable.
- `pac-man.spec`: PyInstaller build specification used to reproduce the application build.

The generated `build/` and `dist/` directories do not need to be committed to Git.

The `Makefile` and `pac-man.spec` are kept in the repository to support rebuilding during peer evaluation.

### 4. Run the Packaged Game

From the project root:

```bash
./dist/pac-man config_file.json
```

To use a custom configuration:

```bash
./dist/pac-man custom_config.json
```

The application validates the provided configuration and applies default values when necessary.

The bundled configuration file does not replace a reviewer-supplied external file. External JSON files remain editable without rebuilding the executable.

### 5. Prepare the Release

The Linux release is organized as follows:

```text
PacMan-Linux/
├── pac-man
├── config_file.json
└── README.txt
```

The `README.txt` contains minimal installation, execution, controls, and configuration instructions.

Create the release folder from the project root:

```bash
mkdir -p release/PacMan-Linux

cp dist/pac-man release/PacMan-Linux/
cp config_file.json release/PacMan-Linux/
cp README.txt release/PacMan-Linux/
```

Create the ZIP archive:

```bash
cd release
zip -r PacMan-Linux.zip PacMan-Linux/
```

The resulting archive is:

```text
release/PacMan-Linux.zip
```

### 6. Install and Run the Downloaded Game

The reviewer downloads and extracts `PacMan-Linux.zip`.

Open a terminal inside the extracted `PacMan-Linux/` folder.

If necessary, make the executable runnable:

```bash
chmod +x pac-man
```

Launch the game:

```bash
./pac-man config_file.json
```

To use another configuration file:

```bash
./pac-man custom_config.json
```

The packaged game does not require a separate Python or Pygame installation.

### 7. Deployment on itch.io

The game is intended to be distributed as a free, unlisted Linux download on [itch.io](https://itch.io/).

Publishing procedure:

1. Sign in to itch.io.
2. Open the creator dashboard.
3. Create a new downloadable project.
4. Set the game title and description.
5. Select Linux as the supported platform.
6. Upload `PacMan-Linux.zip`.
7. Configure the game as free.
8. Set the appropriate unlisted visibility for peer review.
9. Verify that reviewers can access and download the archive.

**Game download:** https://youssef-moufid.itch.io/pac-man

### 8. Packaging Verification

Before distribution, the packaged application should be tested separately from the development environment.

Verification includes:

- The executable launches successfully.
- Menus, fonts, images, and sounds are displayed correctly.
- Configuration loading works.
- Reviewer-provided JSON files are accepted.
- Pac-Man and ghost movement works.
- Collectibles, lives, and scoring work.
- Levels, timers, and cheat features work.
- Highscores are saved in a persistent, writable location.
- The game can be rebuilt using the Makefile or specification.

PyInstaller's temporary extraction directory is used for bundled resources, not permanent highscore storage.

---

## Project Management

The project is developed collaboratively, with responsibilities divided between the game engine and the frontend.

### Game Engine / Backend

Responsible for:

- Configuration and validation.
- Maze generation and population.
- Player movement.
- Ghost AI and pathfinding.
- Game rules and collisions.
- Score, lives, timers, and level progression.
- Cheat functionality.
- Backend testing.

### Frontend

Responsible for:

- Pygame rendering.
- Visual assets and animations.
- Keyboard input.
- Game menus.
- Heads-up display (HUD).
- Game status screens.
- Integrating the interface with GameState.

### Collaboration

Git and GitHub are used for version control and collaborative development.

Feature branches allow team members to work independently before integrating their changes.

Repository: [Pac-Man on GitHub](https://github.com/Youssef01Moufid/Pac-Man)

---

## Resources

### Technical References

- [Python Documentation](https://docs.python.org/3/)
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Python dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [Python enum](https://docs.python.org/3/library/enum.html)
- [Python collections](https://docs.python.org/3/library/collections.html)
- [Breadth-First Search](https://en.wikipedia.org/wiki/Breadth-first_search)
- [PyInstaller Documentation](https://pyinstaller.org/en/stable/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [itch.io Creator Documentation](https://itch.io/docs/creators/)

The assigned A-Maze-ing package was used to generate the maze structures required by the project.

### AI Usage

AI-assisted tools were used during development as learning and debugging aids.

The areas of assistance included:

- Understanding Python concepts and object-oriented design.
- Discussing responsibilities and relationships of engine classes.
- Reviewing movement and ghost AI logic.
- Explaining BFS pathfinding and maze bitmasks.
- Investigating collision detection and smooth movement problems.
- Reviewing configuration validation and error handling.
- Discussing engine/frontend integration.
- Preparing documentation and testing examples.
- Explaining PyInstaller packaging and deployment workflows.

AI suggestions were reviewed and adapted to the project's requirements. The team remains responsible for understanding, testing, and validating the final implementation.

---

## Authors

Developed as part of the **42 curriculum**.

- **ymoufid** — Game Engine / Backend
- **ichokair** — Frontend / Rendering

## License

Distribution and licensing terms will be specified before public release.