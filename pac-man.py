from ui.app import App
from ui.highscores import HighScoreManger
from config.loader import ConfigLoader
from game.gamestate import GameState
import sys


if __name__ == "__main__":
    config_path = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "config_file.json"
    )


    try:
        config = ConfigLoader(config_path).load()
        App(config).run()
    # except Exception as e:
    #     print(f"Error {e}", file=sys.stderr)
    except KeyboardInterrupt:
        print(f"Keyboard Signal send", file=sys.stderr)