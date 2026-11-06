import pygame


class FakeGame:

    def __init__(self, time_limit: float = 30.0) -> None:
        self.score = 0
        self.lives = 3
        self.level = 1
        self.time_left = time_limit
        self.is_over = False
        self._score_clock = 0.0
    

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            self.lives -= 1
            if self.lives <= 0:
                self.is_over = True
    

    def update(self, dt: float) -> None:
        if self.is_over:
            return
        self.time_left = max(0.0, self.time_left - dt)
    
        self._score_clock += dt

        while self._score_clock >= 1.0:
            self._score_clock -= 1
            self.score += 10
        
        if self.time_left <= 0:
            self.is_over = True
    
    def draw(self, surface: pygame.Surface) -> None:
        surface.fill("black")
