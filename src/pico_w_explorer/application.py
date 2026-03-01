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

    def _format_times(self) -> str:
        if len(self._reminder_times) == 1:
            h, m = self._reminder_times[0]
            return "Reminder at %02d:%02d" % (h, m)
        parts = ", ".join("%02d:%02d" % (h, m) for h, m in self._reminder_times)
        return "Reminders at " + parts

    def start(self) -> None:
        self._display.show_text("Connecting to WiFi...")
        hour, minute = self._clock.current_time()
        times_str = self._format_times()
        self._display.show_text(
            "Clock synced\n%02d:%02d\n%s" % (hour, minute, times_str)
        )
        self._display.show_text("Running...\n%s" % times_str)
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
