from pico_w_explorer.colour import Colour, WHITE
from pico_w_explorer.text_spec import TextSpec

DEFAULT_TEXT_SPEC = TextSpec()


class DisplayPort:
    def show_text(self, text: str, x: int = 0, y: int = 0, text_spec: TextSpec = DEFAULT_TEXT_SPEC) -> None:
        raise NotImplementedError

    def draw_rect(self, x: int, y: int, width: int, height: int, colour: Colour = WHITE) -> None:
        raise NotImplementedError
