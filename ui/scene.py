from __future__ import annotations
from abc import ABC, abstractmethod


class Scene(ABC):

    def __init__(self, manager: SceneManger):
        self.manager = manager
        

    @abstractmethod
    def handle_event(self):
        """"""
    
    @abstractmethod
    def update(self):
        """"""
    
    @abstractmethod
    def draw(self):
        """"""


class SceneManger:
    
    def __init__(
        self,
        ):
        self._stack: list[Scene] = []
        self.running: bool = True

    @property
    def current(self):
        return self._stack[-1] if self._stack else None
    
    
    def push(self, scene: Scene):
        
        self._stack.append(scene)
    
    
    def pop(self):

        if self._stack:
            self._stack.pop()
        else:
            self.running = False
    
    
    def replace(self, scene: Scene):
        if self._stack:
            self._stack.pop()
        self._stack.append(scene)

    
    def quit(self):
        self.running = False
