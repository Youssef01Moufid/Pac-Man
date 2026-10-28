"""Run the main menu on its own: python3 menu_demo.py."""

import sys

from app.app import APP


def main() -> int:
    """Start the app; never show a traceback to the user."""
    try:
        APP().run()
    except Exception as exc:  # last safety net, required by the subject
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
