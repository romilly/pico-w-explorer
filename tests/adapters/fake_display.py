from pico_w_explorer.colour import Colour, WHITE
from pico_w_explorer.ports import DisplayPort


class FakeDisplay(DisplayPort):
    def __init__(self) -> None:
        self.last_text: str | None = None
        self.last_colour: Colour = WHITE
        self.last_y: int = 0
        self.texts: list[str] = []
        self.rects: list[tuple[int, int, int, int, Colour]] = []

    def show_text(self, text: str, x: int = 0, y: int = 0, colour: Colour = WHITE, scale: float = 1) -> None:
        self.last_text = text
        self.last_colour = colour
        self.last_y = y
        self.texts.append(text)

    def draw_rect(self, x: int, y: int, width: int, height: int, colour: Colour = WHITE) -> None:
        self.rects.append((x, y, width, height, colour))
