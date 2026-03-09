from pico_w_explorer.ports.display import DisplayPort


class Widget:
    def __init__(self, display_port: DisplayPort):
        self._display_port = display_port

class Text(Widget):
    def __init__(self, display_port: DisplayPort, x, y):
        super().__init__(display_port=display_port)
        self._x = x
        self._y = y

    def text(self, contents: str):
        self._display_port.show_text(contents, self._x, self._y)