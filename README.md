# Pac-Man — 42 Project

*This project has been created as part of the 42 curriculum by ymoufid, ichokair.*

## Description

Pac-Man is a maze-based arcade game developed in Python using Pygame.

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

## Instructions

### Requirements

- Python 3.10 or later, subject to dependency compatibility
- `uv` package manager
- Pygame
- The assigned A-Maze-ing package

### Installation

Clone the repository:

```bash
git clone https://github.com/Youssef01Moufid/Pac-Man
cd REPOSITORY
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

Alternatively, use the Makefile if configured:

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

*These are the controls used by the current engine test. Update this section if the final frontend uses different shortcuts.*

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

## Configuration

The game uses a JSON configuration file, typically named `config_file.json`.

The configuration is loaded through `ConfigLoader`, which validates input values and applies defaults when necessary.

### Global configuration

| Parameter | Description | Default |
|---|---|---|
| `highscore_filename` | File used to store highscores | `highscores.json` |
| `lives` | Initial number of lives | 3 |
| `points_per_pacgum` | Points for a regular Pac-Gum | 10 |
| `points_per_super_pacgum` | Points for a Super Pac-Gum | 50 |
| `points_per_ghost` | Points for eating a frightened ghost | 200 |
| `seed` | Seed used for the first level | 42 |
| `levels` | List of level configurations | 10 default levels |

### Per-level configuration

Each level has its own parameters.

| Parameter | Description | Default |
|---|---|---|
| `width` | Maze width, odd integer between 9 and 51 | 21 |
| `height` | Maze height, odd integer between 9 and 51 | 21 |
| `pacgum` | Requested number of regular Pac-Gums | 42 |
| `level_max_time` | Time limit in seconds, between 10 and 600 | 90 |

### Example

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

The example shows two explicitly configured levels. `ConfigLoader` automatically adds default levels until the minimum of 10 is reached.

The loader also supports `#` comments in configuration files, validates data types, and records warnings for invalid values.

## Highscore System

The game configuration defines the highscore file through `highscore_filename`.

The highscore feature is intended to record player scores and allow comparison between game sessions.

**Implementation status:** Update this section with the actual highscore storage format, player-name rules, and persistence behavior once the highscore component has been integrated.

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

## Implementation

The project separates game logic, movement, maze generation, configuration, and rendering into dedicated components.

### Movement System

The `Movement` class validates movement between neighboring maze cells using the wall bitmasks.

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

## General Software Architecture

The project uses a modular architecture with clear separation of responsibilities.

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

It can obtain the smooth position of Pac-Man using:

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

## Project Packaging

The final application is intended to be packaged for distribution through a public game platform such as itch.io.

The packaging process should include:

- A launchable application.
- Required runtime dependencies.
- Game assets.
- Configuration files.
- Instructions for players.
- Support for persistent highscore storage.

The Git repository must contain the packaging script or specification at its root, allowing the application to be rebuilt during peer evaluation.

**Implementation status:** Add the final build command, supported operating systems, and download link after packaging is completed.

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

Project management documentation can be found here:

**[Project Management](./project_management/)**

*Update this link to match the actual directory in your repository.*

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
- Discussing the responsibilities and relationships of engine classes.
- Reviewing movement and ghost AI logic.
- Explaining BFS pathfinding and maze bitmasks.
- Investigating collision detection and smooth movement problems.
- Reviewing configuration validation and error handling.
- Discussing engine/frontend integration.
- Preparing documentation and testing examples.

AI suggestions were reviewed and adapted to the project's requirements. The team remains responsible for understanding, testing, and validating the final implementation.

---

## Authors

Developed as part of the **42 curriculum**.

- **[login1]** — Game Engine / Backend
- **[login2]** — Frontend / Rendering

## License

Add the project's license or distribution terms here before publishing.# Pac-Man — 42 Project

*This project has been created as part of the 42 curriculum by [login1](https://github.com/USERNAME1), [login2](https://github.com/USERNAME2).*

## Description

Pac-Man is a maze-based arcade game developed in Python using Pygame.

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

## Instructions

### Requirements

- Python 3.10 or later, subject to dependency compatibility
- `uv` package manager
- Pygame
- The assigned A-Maze-ing package

### Installation

Clone the repository:

```bash
git clone https://github.com/USERNAME/REPOSITORY.git
cd REPOSITORY
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

Alternatively, use the Makefile if configured:

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

*These are the controls used by the current engine test. Update this section if the final frontend uses different shortcuts.*

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

## Configuration

The game uses a JSON configuration file, typically named `config_file.json`.

The configuration is loaded through `ConfigLoader`, which validates input values and applies defaults when necessary.

### Global configuration

| Parameter | Description | Default |
|---|---|---|
| `highscore_filename` | File used to store highscores | `highscores.json` |
| `lives` | Initial number of lives | 3 |
| `points_per_pacgum` | Points for a regular Pac-Gum | 10 |
| `points_per_super_pacgum` | Points for a Super Pac-Gum | 50 |
| `points_per_ghost` | Points for eating a frightened ghost | 200 |
| `seed` | Seed used for the first level | 42 |
| `levels` | List of level configurations | 10 default levels |

### Per-level configuration

Each level has its own parameters.

| Parameter | Description | Default |
|---|---|---|
| `width` | Maze width, odd integer between 9 and 51 | 21 |
| `height` | Maze height, odd integer between 9 and 51 | 21 |
| `pacgum` | Requested number of regular Pac-Gums | 42 |
| `level_max_time` | Time limit in seconds, between 10 and 600 | 90 |

### Example

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

The example shows two explicitly configured levels. `ConfigLoader` automatically adds default levels until the minimum of 10 is reached.

The loader also supports `#` comments in configuration files, validates data types, and records warnings for invalid values.

## Highscore System

The game configuration defines the highscore file through `highscore_filename`.

The highscore feature is intended to record player scores and allow comparison between game sessions.

**Implementation status:** Update this section with the actual highscore storage format, player-name rules, and persistence behavior once the highscore component has been integrated.

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

## Implementation

The project separates game logic, movement, maze generation, configuration, and rendering into dedicated components.

### Movement System

The `Movement` class validates movement between neighboring maze cells using the wall bitmasks.

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

## General Software Architecture

The project uses a modular architecture with clear separation of responsibilities.

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

It can obtain the smooth position of Pac-Man using:

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

## Project Packaging

The final application is intended to be packaged for distribution through a public game platform such as itch.io.

The packaging process should include:

- A launchable application.
- Required runtime dependencies.
- Game assets.
- Configuration files.
- Instructions for players.
- Support for persistent highscore storage.

The Git repository must contain the packaging script or specification at its root, allowing the application to be rebuilt during peer evaluation.

**Implementation status:** Add the final build command, supported operating systems, and download link after packaging is completed.

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

Project management documentation can be found here:

**[Project Management](https://github.com/Youssef01Moufid/Pac-Man)**

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
- Discussing the responsibilities and relationships of engine classes.
- Reviewing movement and ghost AI logic.
- Explaining BFS pathfinding and maze bitmasks.
- Investigating collision detection and smooth movement problems.
- Reviewing configuration validation and error handling.
- Discussing engine/frontend integration.
- Preparing documentation and testing examples.

AI suggestions were reviewed and adapted to the project's requirements. The team remains responsible for understanding, testing, and validating the final implementation.

---

## Authors

Developed as part of the **42 curriculum**.

- **[ymoufid]** — Game Engine / Backend
- **[ichokair]** — Frontend / Rendering

## License

Add the project's license or distribution terms here before publishing.