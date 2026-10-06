from pathlib import Path
from .defaults import DefaultsSchema
from .model import Config


class ConfigLoader:

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def _validate_extension(self) -> bool:
        pass

    def _read_and_strip_comment(self) -> str:
        pass
    
    def _parse_json(self, clean_text: str) -> dict[str, Any]:
        pass

    def load(self) -> Config:
        pass
