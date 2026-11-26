import sys
import os

from pathlib import Path


class PathChecker:
    def project_root(self) -> str:
        bundle_dir = getattr(sys, "_MEIPASS", None)
        if bundle_dir is not None:
            return str(bundle_dir)

        file_root = Path(__file__).resolve().parent.parent

        return str(file_root)

    def ressource_path(self, *parts: str) -> str:
        return os.path.join(self.project_root(), *parts)


FONT_URL = PathChecker().ressource_path(
    "assets", "fonts", "PressStart2P-Regular.ttf"
)
