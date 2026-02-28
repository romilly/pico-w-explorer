from pico_w_explorer.ports import BuzzerPort, ButtonPort, ClockPort, LedPort


class FocusReminder:
    def __init__(
        self,
        clock: ClockPort,
        buzzer: BuzzerPort,
        led: LedPort,
        button: ButtonPort,
        reminder_hour: int,
        reminder_minute: int,
    ) -> None:
        self._clock = clock
        self._buzzer = buzzer
        self._led = led
        self._button = button
        self._reminder_hour = reminder_hour
        self._reminder_minute = reminder_minute

    def tick(self) -> None:
        pass
