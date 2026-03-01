from pico_w_explorer.application import Application
from tests.adapters.fake_buzzer import FakeBuzzer
from tests.adapters.fake_button import FakeButton
from tests.adapters.fake_clock import FakeClock
from tests.adapters.fake_display import FakeDisplay
from tests.adapters.fake_led import FakeLed


class ApplicationBuilder:
    def __init__(self) -> None:
        self.clock = FakeClock()
        self.buzzer = FakeBuzzer()
        self.led = FakeLed()
        self.button = FakeButton()
        self.display = FakeDisplay()
        self._reminder_hour = 14
        self._reminder_minute = 0

    def with_clock(self, clock: FakeClock) -> 'ApplicationBuilder':
        self.clock = clock
        return self

    def with_buzzer(self, buzzer: FakeBuzzer) -> 'ApplicationBuilder':
        self.buzzer = buzzer
        return self

    def with_led(self, led: FakeLed) -> 'ApplicationBuilder':
        self.led = led
        return self

    def with_button(self, button: FakeButton) -> 'ApplicationBuilder':
        self.button = button
        return self

    def with_display(self, display: FakeDisplay) -> 'ApplicationBuilder':
        self.display = display
        return self

    def with_reminder_time(self, hour: int, minute: int) -> 'ApplicationBuilder':
        self._reminder_hour = hour
        self._reminder_minute = minute
        return self

    def build(self) -> Application:
        return Application(
            clock=self.clock,
            buzzer=self.buzzer,
            led=self.led,
            button=self.button,
            display=self.display,
            reminder_hour=self._reminder_hour,
            reminder_minute=self._reminder_minute,
        )
