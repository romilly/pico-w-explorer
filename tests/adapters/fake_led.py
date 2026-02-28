from pico_w_explorer.ports import LedPort


class FakeLed(LedPort):
    def __init__(self) -> None:
        self.on = False

    def flash_on(self) -> None:
        self.on = True

    def flash_off(self) -> None:
        self.on = False
