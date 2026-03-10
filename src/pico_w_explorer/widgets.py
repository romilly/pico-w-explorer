from pico_w_explorer.colour import Colour, WHITE, BLACK
from pico_w_explorer.ports.display import DisplayPort

TEXT_HEIGHT = 32


class Widget:
    def __init__(self, display_port: DisplayPort) -> None:
        self._display_port = display_port

class Text(Widget):
    def __init__(self, display_port: DisplayPort, x: int, y: int, colour: Colour = WHITE) -> None:
        super().__init__(display_port=display_port)
        self._x = x
        self._y = y
        self._colour = colour
        self._previous_text: str | None = None

    def text(self, contents: str) -> None:
        new_width = self._display_port.measure_text(contents)
        if self._previous_text is not None:
            old_width = self._display_port.measure_text(self._previous_text)
            clear_width = max(old_width, new_width)
        else:
            clear_width = new_width
        self._display_port.draw_rect(self._x, self._y - 11, clear_width + 2, TEXT_HEIGHT, BLACK)
        self._display_port.show_text(contents, self._x, self._y + 1, colour=self._colour)
        self._previous_text = contents
