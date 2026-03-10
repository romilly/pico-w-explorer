from pico_w_explorer.colour import Colour, WHITE


class DisplayPort:
    def show_text(self, text: str, x: int = 0, y: int = 0, colour: Colour = WHITE, scale: float = 1) -> None:
        raise NotImplementedError

    def draw_rect(self, x: int, y: int, width: int, height: int, colour: Colour = WHITE) -> None:
        raise NotImplementedError
