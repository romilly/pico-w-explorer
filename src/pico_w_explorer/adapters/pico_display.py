from picographics import PicoGraphics, DISPLAY_PICO_W_EXPLORER  # type: ignore[import-not-found]

from pico_w_explorer.ports import DisplayPort


class PicoDisplay(DisplayPort):
    def __init__(self) -> None:
        self._display = PicoGraphics(display=DISPLAY_PICO_W_EXPLORER)
        self._black = self._display.create_pen(0, 0, 0)
        self._white = self._display.create_pen(255, 255, 255)

    def show_text(self, text: str) -> None:
        self._display.set_pen(self._black)
        self._display.clear()
        self._display.set_pen(self._white)
        self._display.text(text, 20, 20, 200)
        self._display.update()
