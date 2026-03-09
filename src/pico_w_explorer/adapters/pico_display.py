from picographics import PicoGraphics, DISPLAY_PICO_W_EXPLORER  # type: ignore[import-not-found]

from pico_w_explorer.colour import Colour, WHITE
from pico_w_explorer.ports import DisplayPort

DISPLAY = PicoGraphics(display=DISPLAY_PICO_W_EXPLORER)
BLACK_PEN = DISPLAY.create_pen(0, 0, 0)

class PicoDisplay(DisplayPort):
    def __init__(self, title: str = "") -> None:
        DISPLAY.set_pen(BLACK_PEN)
        DISPLAY.clear()

    def show_text(self, text: str, x: int = 20, y: int = 20, colour: Colour = WHITE, scale: int = 1) -> None:
        DISPLAY.set_font("sans")
        DISPLAY.set_thickness(2)
        width = DISPLAY.measure_text(text, scale)
        DISPLAY.set_pen(BLACK_PEN)
        DISPLAY.rectangle(x, y - 10, width, 30)
        pen = DISPLAY.create_pen(colour.red, colour.green, colour.blue)
        DISPLAY.set_pen(pen)
        DISPLAY.text(text, x, y, 300, scale)
        DISPLAY.update()
