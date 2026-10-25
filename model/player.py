from movment import Movement, Direction

class Player:

    def __init__(
            self,
            row: int,
            col: int,
            direction: Direction,
            desired_direction: Direction,
            speed: int, 
            rogress: float
        ) -> None:

        