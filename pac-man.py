import logging
from pathlib import Path

# Adjust import path to match your project layout
from config.loader import ConfigLoader

# Enable logging to see any warnings/fallbacks if values in the file are invalid
logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")


def main() -> None:
    # 1. Target your specific config file
    config_path = Path("/home/ymoufid/Desktop/pac_man/config_file.json")

    print(f"Loading configuration from: {config_path}\n")

    # 2. Instantiate loader and load the config
    loader = ConfigLoader(config_path)
    config = loader.load()

    # 3. Print the resolved attributes
    print("=" * 40)
    print("RESOLVED CONFIGURATION")
    print("=" * 40)
    print(f"lives                   = {config.lives}")
    print(f"pacgum                  = {config.pacgum}")
    print(f"highscore_filename      = {config.highscore_filename}")
    print(f"seed                    = {config.seed}")
    print(f"level_max_time          = {config.level_max_time}")
    print(f"points_per_pacgum       = {config.points_per_pacgum}")
    print(f"points_per_super_pacgum = {config.points_per_super_pacgum}")
    print(f"points_per_ghost        = {config.points_per_ghost}")
    print(f"levels count            = {len(config.levels)}")
    print("-" * 40)

    # 4. Print individual levels
    for i, level in enumerate(config.levels, start=1):
        print(f"Level {i}: width={level.width}, height={level.height}")
    
    print("=" * 40)


if __name__ == "__main__":
    main()