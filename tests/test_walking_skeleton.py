from tests.adapters.fake_buzzer import FakeBuzzer
from tests.adapters.fake_button import FakeButton
from tests.adapters.fake_clock import FakeClock
from tests.adapters.fake_led import FakeLed
from tests.builders import ApplicationBuilder


class TestFullApplicationLifecycle:
    def setup_method(self) -> None:
        self.clock = FakeClock()
        self.buzzer = FakeBuzzer()
        self.led = FakeLed()
        self.button = FakeButton()

    def build_app(self, start_hour: int = 13, start_minute: int = 0,
                  reminder_times: list[tuple[int, int]] | None = None) -> None:
        builder = (
            ApplicationBuilder()
            .with_clock(self.clock)
            .with_buzzer(self.buzzer)
            .with_led(self.led)
            .with_button(self.button)
            .with_time(start_hour, start_minute)
        )
        if reminder_times is not None:
            builder = builder.with_reminder_times(reminder_times)
        self.app = builder.build()
        self.app.start()

    def wait(self, minutes: int = 1) -> None:
        for _ in range(minutes):
            self.clock.tick()
            self.app.tick()

    def press_button(self) -> None:
        self.button.press()

    def release_button(self) -> None:
        self.button.release()

    def assert_alerting(self) -> None:
        assert self.buzzer.on is True
        assert self.led.on is True

    def assert_silent(self) -> None:
        assert self.buzzer.on is False
        assert self.led.on is False

    def test_single_alert_lifecycle(self) -> None:
        self.build_app()

        # Before reminder — silent
        self.wait(minutes=30)
        self.assert_silent()

        # At reminder time (14:00) — alerting
        self.wait(minutes=30)
        self.assert_alerting()

        # Button press — dismissed
        self.press_button()
        self.wait()
        self.assert_silent()

        # Stays dismissed after release
        self.release_button()
        self.wait()
        self.assert_silent()

    def test_multiple_alerts_lifecycle(self) -> None:
        self.build_app(start_hour=13, start_minute=0,
                       reminder_times=[(14, 0), (15, 0)])

        # Before first reminder — silent
        self.wait(minutes=30)
        self.assert_silent()

        # At 14:00 — first alert fires
        self.wait(minutes=30)
        self.assert_alerting()

        # Dismiss first alert
        self.press_button()
        self.wait()
        self.assert_silent()
        self.release_button()

        # Still silent — second alert not yet due
        self.wait(minutes=29)
        self.assert_silent()

        # At 15:00 — second alert fires
        self.wait(minutes=30)
        self.assert_alerting()

        # Dismiss second alert
        self.press_button()
        self.wait()
        self.assert_silent()
