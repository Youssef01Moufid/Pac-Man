"""Class Responsible to manage the scores scored in the game """

import json
from typing import Any
import sys

class HighScoreManger:

    MAX_ENTIRES = 10
    MAX_LENGHT_NAME = 10

    def __init__(self, path: str) -> None:
        self._path = path
        self._entries: list[tuple[str, int]] = []
    

    def load(self) -> None:
        # the goal is top open a file and the check get the entire data with in it
        self._entries = []

        try:
            with open(self._path, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"No highscore file at '{self._path}', starting empty.",
                  file=sys.stderr)
            return
        except json.JSONDecodeError:
            print(f"Highscore file '{self._path}' is corrupted, "
                  "starting empty.", file=sys.stderr)
            return
        except OSError as e:
            print(f"Cannot read highscore file '{self._path}': {e}",
                  file=sys.stderr)
            return
        
        if not isinstance(data, list):
            print(f"Highscore file '{self._path}' is not a list, "
                  "starting empty.", file=sys.stderr)
            return
        
        valid: list[tuple[str, int]] = []
        for element in data:
            entry = self._parse_element(element)
            if entry is None:
                print(f"Skipping invalid highscore entry: {element!r}",
                      file=sys.stderr)
                continue
            valid.append(entry)

        self._entries = self._rank(valid)

    def add(self, name: str, score: int) -> None:
        entry = self._parse_element({"name": name, "score": score})
        if entry is None:
            raise ValueError(f"Invalid highscore: {name!r}, {score!r}")
        self._entries = self._rank(self._entries + [entry])


    def save(self) -> None:
        """ write to list on the disk never raise the disk Errors"""
        data = [{"name": name, "score": score} for name, score in self._entries]
        try:
            with open(self._path, 'w', encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except OSError as e:
            print(f"Cannot save highscores to '{self._path}': {e}",
                  file=sys.stderr)

    
    def is_highscore(self, score: int) -> bool:
        """ Check the score if is valid to be store as a highscore"""
        if score < 0:
            return False
        
        if len(self._entries) < self.MAX_ENTIRES:
            return True
        
        return score > self._entries[-1][1]
    

    @property
    def entries(self):
        """ Return a copy of the list of the highest score """
        return list(self._entries)
    

    def _parse_element(self, element: Any) -> tuple[str, int] | None:
        """ check the element is a dictionary with name key and score key"""
        if not isinstance(element, dict):
            return None
        
        name = element.get("name")
        score = element.get("score")

        if not isinstance(name, str):
            return None
        name = name.strip()
        if not name or len(name) >  self.MAX_LENGHT_NAME:
            return None
        
        if isinstance(score, bool) or not isinstance(score, int):
            return None
        if score < 0:
            return None
        return (name, score)
    

    def _rank(self, valid_entries: list[tuple[str, int]]) -> list[tuple[str, int]]:
        """ rank from the highes score to lowest and return the max entries"""
        ranked = sorted(valid_entries, key=lambda e: e[1], reverse=True)
        return ranked[:self.MAX_ENTIRES]
