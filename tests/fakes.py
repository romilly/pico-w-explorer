class FakeClock:
    def __init__(self, hour: int = 0, minute: int = 0) -> None:
        self._hour = hour
        self._minute = minute

    def set_time(self, hour: int, minute: int) -> None:
        self._hour = hour
        self._minute = minute

    def current_time(self) -> tuple[int, int]:
        return (self._hour, self._minute)


class FakeBuzzer:
    def __init__(self) -> None:
        self.on = False

    def beep_on(self) -> None:
        self.on = True

    def beep_off(self) -> None:
        self.on = False


class FakeLed:
    def __init__(self) -> None:
        self.on = False

    def flash_on(self) -> None:
        self.on = True

    def flash_off(self) -> None:
        self.on = False


class FakeButton:
    def __init__(self) -> None:
        self._pressed = False

    def press(self) -> None:
        self._pressed = True

    def release(self) -> None:
        self._pressed = False

    def is_pressed(self) -> bool:
        return self._pressed
