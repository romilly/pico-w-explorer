from pico_w_explorer.ports import BuzzerPort


class FakeBuzzer(BuzzerPort):
    def __init__(self) -> None:
        self.on = False

    def beep_on(self) -> None:
        self.on = True

    def beep_off(self) -> None:
        self.on = False
