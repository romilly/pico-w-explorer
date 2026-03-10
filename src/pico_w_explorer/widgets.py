from pico_w_explorer.colour import BLACK
from pico_w_explorer.ports.display import DisplayPort
from pico_w_explorer.text_spec import TextSpec

TEXT_HEIGHT = 32


class Widget:
    def __init__(self, display_port: DisplayPort) -> None:
        self._display_port = display_port

class Text(Widget):
    def __init__(self, display_port: DisplayPort, x: int, y: int, width: int, text_spec: TextSpec | None = None) -> None:
        super().__init__(display_port=display_port)
        self._x = x
        self._y = y
        self._width = width
        self._text_spec = text_spec if text_spec is not None else TextSpec()

    def text(self, contents: str) -> None:
        self._display_port.draw_rect(self._x, self._y - 11, self._width, TEXT_HEIGHT, BLACK)
        self._display_port.show_text(contents, self._x, self._y + 1, text_spec=self._text_spec)
