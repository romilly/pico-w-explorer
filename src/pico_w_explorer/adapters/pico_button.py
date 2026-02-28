from pimoroni import Button  # type: ignore[import-not-found]

from pico_w_explorer.ports import ButtonPort


class PicoButton(ButtonPort):
    def __init__(self, pin: int = 6) -> None:
        self._button = Button(pin)

    def is_pressed(self) -> bool:
        return self._button.is_pressed  # type: ignore[no-any-return]
