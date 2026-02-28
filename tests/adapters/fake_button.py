from pico_w_explorer.ports import ButtonPort


class FakeButton(ButtonPort):
    def __init__(self) -> None:
        self._pressed = False

    def press(self) -> None:
        self._pressed = True

    def release(self) -> None:
        self._pressed = False

    def is_pressed(self) -> bool:
        return self._pressed
