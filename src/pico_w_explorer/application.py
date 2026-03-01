import time

from pico_w_explorer.focus_reminder import FocusReminder
from pico_w_explorer.ports import BuzzerPort, ButtonPort, ClockPort, DisplayPort, LedPort


class Application:
    def __init__(
        self,
        clock: ClockPort,
        buzzer: BuzzerPort,
        led: LedPort,
        button: ButtonPort,
        display: DisplayPort,
        reminder_hour: int,
        reminder_minute: int,
        tick_interval: float = 0.5,
    ) -> None:
        self._clock = clock
        self._buzzer = buzzer
        self._led = led
        self._button = button
        self._display = display
        self._reminder_hour = reminder_hour
        self._reminder_minute = reminder_minute
        self._tick_interval = tick_interval

    def start(self) -> None:
        self._display.show_text("Connecting to WiFi...")
        hour, minute = self._clock.current_time()
        self._display.show_text(
            "Clock synced\n%02d:%02d\nReminder at %02d:%02d"
            % (hour, minute, self._reminder_hour, self._reminder_minute)
        )
        self._display.show_text(
            "Running...\nReminder at %02d:%02d"
            % (self._reminder_hour, self._reminder_minute)
        )
        self._reminder = FocusReminder(
            self._clock, self._buzzer, self._led, self._button,
            self._reminder_hour, self._reminder_minute,
        )

    def tick(self) -> None:
        self._reminder.tick()

    def run(self) -> None:
        self.start()
        while True:
            self.tick()
            time.sleep(self._tick_interval)
