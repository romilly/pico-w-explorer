from pico_w_explorer.colour import Colour, WHITE

VALID_FONTS = ("sans", "gothic", "cursive", "serif_italic", "serif")


class TextSpec:
    def __init__(
        self,
        font: str = "sans",
        colour: Colour = WHITE,
        thickness: int = 2,
        scale: float = 1,
    ) -> None:
        if font not in VALID_FONTS:
            raise ValueError(f"Invalid font: {font!r}. Must be one of {VALID_FONTS}")
        self.font = font
        self.colour = colour
        self.thickness = thickness
        self.scale = scale
