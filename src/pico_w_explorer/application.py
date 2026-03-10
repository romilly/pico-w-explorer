import time

from pico_w_explorer.colour import RED, BLUE
from pico_w_explorer.focus_reminder import FocusReminder
from pico_w_explorer.ports import BuzzerPort, ButtonPort, ClockPort, DisplayPort, LedPort
from pico_w_explorer.widgets import Text


class ApplicationConfig:
    def __init__(
        self,
        clock: ClockPort,
        buzzer: BuzzerPort,
        led: LedPort,
        button: ButtonPort,
        display: DisplayPort,
        reminder_times: list[tuple[int, int]],
        tick_interval: float = 0.5,
    ) -> None:
        self.clock = clock
        self.buzzer = buzzer
        self.led = led
        self.button = button
        self.display = display
        self.reminder_times = reminder_times
        self.tick_interval = tick_interval


class Application:
    def __init__(self, config: ApplicationConfig) -> None:
        self._clock = config.clock
        self._buzzer = config.buzzer
        self._led = config.led
        self._button = config.button
        self._display = config.display
        self._reminder_times = sorted(config.reminder_times)
        self._tick_interval = config.tick_interval
        self._status = Text(self._display, 3, 20)
        self._time_display = Text(self._display, 160, 20)
        self._reminders =Text(self._display, 3, 60, colour = BLUE)
        self._times = Text(self._display, 3, 100, colour = RED)

    def _format_current_time(self) -> str:
        hour, minute, second = self._clock.current_time()
        return "%02d:%02d:%02d" % (hour, minute, second)

    def _format_times(self) -> str:
        parts = ", ".join("%02d:%02d" % (h, m) for h, m in self._reminder_times)
        return parts
    
    def status(self, contents: str):
        self._status.text(contents)

    def reminders(self):
        self._reminders.text("Reminders:")

    def times(self, times: str):
        self._times.text(times)

    def start(self) -> None:
        self.status("Running...")
        self.reminders()
        self.times(self._format_times())
        self._time_display.text(self._format_current_time())
        self._reminder = FocusReminder(
            self._clock, self._buzzer, self._led, self._button,
            reminder_times=self._reminder_times,
        )

    def tick(self) -> None:
        self._time_display.text(self._format_current_time())
        self._reminder.tick()

    def run(self) -> None:
        self.start()
        while True:
            self.tick()
            time.sleep(self._tick_interval)
