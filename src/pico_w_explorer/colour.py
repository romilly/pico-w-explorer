class Colour:
    def __init__(self, red: int, green: int, blue: int) -> None:
        self.red = red
        self.green = green
        self.blue = blue


WHITE = Colour(255, 255, 255)
BLACK = Colour(0, 0, 0)
RED = Colour(255, 0, 0)
GREEN = Colour(0, 255, 0)
BLUE = Colour(0, 0, 255)
YELLOW = Colour(255, 255, 0)
