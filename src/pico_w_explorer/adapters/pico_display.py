from picographics import PicoGraphics, DISPLAY_PICO_W_EXPLORER  # type: ignore[import-not-found]

from pico_w_explorer.colour import Colour, WHITE
from pico_w_explorer.ports import DisplayPort
from pico_w_explorer.ports.display import DEFAULT_TEXT_SPEC
from pico_w_explorer.text_spec import TextSpec

DISPLAY = PicoGraphics(display=DISPLAY_PICO_W_EXPLORER)
BLACK_PEN = DISPLAY.create_pen(0, 0, 0)

class PicoDisplay(DisplayPort):
    def __init__(self, title: str = "") -> None:
        DISPLAY.set_pen(BLACK_PEN)
        DISPLAY.clear()

    def show_text(self, text: str, x: int = 20, y: int = 20, text_spec: TextSpec = DEFAULT_TEXT_SPEC) -> None:
        DISPLAY.set_font(text_spec.font)
        DISPLAY.set_thickness(text_spec.thickness)
        pen = DISPLAY.create_pen(*text_spec.colour.rgb())
        DISPLAY.set_pen(pen)
        DISPLAY.text(text, x, y, 300, text_spec.scale)
        DISPLAY.update()

    def draw_rect(self, x: int, y: int, width: int, height: int, colour: Colour = WHITE) -> None:
        pen = DISPLAY.create_pen(*colour.rgb())
        DISPLAY.set_pen(pen)
        DISPLAY.rectangle(x, y, width, height)
        DISPLAY.update()
