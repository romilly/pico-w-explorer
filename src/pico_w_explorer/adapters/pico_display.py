from picographics import PicoGraphics, DISPLAY_PICO_W_EXPLORER  # type: ignore[import-not-found]

from pico_w_explorer.ports import DisplayPort

DISPLAY = PicoGraphics(display=DISPLAY_PICO_W_EXPLORER)
BLACK_  = DISPLAY.create_pen(0, 0, 0)
WHITE   = DISPLAY.create_pen(255, 255, 255)

class PicoDisplay(DisplayPort):
    def __init__(self, title = "") -> None:
        DISPLAY.set_pen(BLACK_)
        DISPLAY.clear()

    def show_text(self, text: str, x = 20, y = 20, colour = WHITE, scale = 1) -> None:
        DISPLAY.set_pen(colour)
        DISPLAY.set_font("sans")
        DISPLAY.set_thickness(2)
        DISPLAY.text(text, x, y, 300, scale)
        DISPLAY.update()
