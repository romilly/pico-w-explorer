import time

from pico_w_explorer.focus_reminder import FocusReminder
from pico_w_explorer.ports import BuzzerPort, ButtonPort, ClockPort, DisplayPort, LedPort
from pico_w_explorer.widgets import Text


class Application:
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
        self._clock = clock
        self._buzzer = buzzer
        self._led = led
        self._button = button
        self._display = display
        self._reminder_times = sorted(reminder_times)
        self._tick_interval = tick_interval
        self._status = Text(display, 3, 20)
        self._reminders =Text(display, 3, 60)
        self._times = Text(display, 3, 100)

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
        self._reminder = FocusReminder(
            self._clock, self._buzzer, self._led, self._button,
            reminder_times=self._reminder_times,
        )

    def tick(self) -> None:
        self._reminder.tick()

    def run(self) -> None:
        self.start()
        while True:
            self.tick()
            time.sleep(self._tick_interval)
