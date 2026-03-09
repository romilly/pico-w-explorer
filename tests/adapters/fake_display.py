from pico_w_explorer.colour import Colour, WHITE
from pico_w_explorer.ports import DisplayPort


class FakeDisplay(DisplayPort):
    def __init__(self) -> None:
        self.last_text: str | None = None
        self.last_colour: Colour = WHITE
        self.texts: list[str] = []

    def show_text(self, text: str, x: int = 0, y: int = 0, colour: Colour = WHITE, scale: int = 1) -> None:
        self.last_text = text
        self.last_colour = colour
        self.texts.append(text)
