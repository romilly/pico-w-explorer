from pico_w_explorer.colour import Colour, WHITE
from pico_w_explorer.ports.display import DisplayPort


class Widget:
    def __init__(self, display_port: DisplayPort) -> None:
        self._display_port = display_port

class Text(Widget):
    def __init__(self, display_port: DisplayPort, x: int, y: int, colour: Colour = WHITE) -> None:
        super().__init__(display_port=display_port)
        self._x = x
        self._y = y
        self._colour = colour

    def text(self, contents: str) -> None:
        self._display_port.show_text(contents, self._x, self._y, colour=self._colour)