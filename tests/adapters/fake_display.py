from pico_w_explorer.colour import Colour, WHITE
from pico_w_explorer.ports import DisplayPort
from pico_w_explorer.ports.display import DEFAULT_TEXT_SPEC
from pico_w_explorer.text_spec import TextSpec


class FakeDisplay(DisplayPort):
    def __init__(self) -> None:
        self.last_text: str | None = None
        self.last_text_spec: TextSpec = DEFAULT_TEXT_SPEC
        self.last_y: int = 0
        self.texts: list[str] = []
        self.rects: list[tuple[int, int, int, int, Colour]] = []

    def show_text(self, text: str, x: int = 0, y: int = 0, text_spec: TextSpec = DEFAULT_TEXT_SPEC) -> None:
        self.last_text = text
        self.last_text_spec = text_spec
        self.last_y = y
        self.texts.append(text)

    def last_colour(self) -> Colour:
        return self.last_text_spec.colour

    def draw_rect(self, x: int, y: int, width: int, height: int, colour: Colour = WHITE) -> None:
        self.rects.append((x, y, width, height, colour))
